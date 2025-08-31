"""
Content-based Recommendation Engine
Dựa trên dữ liệu tracking của user để gợi ý sách tương tự
"""
from django.db import connection
from collections import defaultdict, Counter
import re

class RecommendationEngine:
    """
    Content-based recommendation engine sử dụng:
    1. Tracking data từ user activities
    2. Category preferences
    3. Author preferences  
    4. Price range preferences
    """
    
    def __init__(self):
        self.user_preferences = {}
        self.book_features = {}
        
    def get_user_tracking_data(self, user_id):
        """Lấy dữ liệu tracking của user từ activities"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT BookID, Action, COUNT(*) as frequency
                FROM useractivity
                WHERE CustomerID = %s
                GROUP BY BookID, Action
                ORDER BY frequency DESC
            """, [user_id])
            
            tracking_data = {}
            for row in cursor.fetchall():
                book_id, action, frequency = row
                if book_id not in tracking_data:
                    tracking_data[book_id] = {}
                tracking_data[book_id][action] = frequency
                
            return tracking_data
    
    def build_user_profile(self, user_id):
        """Xây dựng profile user dựa trên tracking data"""
        tracking_data = self.get_user_tracking_data(user_id)
        
        if not tracking_data:
            return None
            
        # Lấy thông tin sách user đã tương tác
        with connection.cursor() as cursor:
            book_ids = list(tracking_data.keys())
            if not book_ids:
                return None
                
            placeholders = ','.join(['%s'] * len(book_ids))
            cursor.execute(f"""
                SELECT b.BookID, b.CategoryID, b.AuthorID, b.Price, c.CategoryName, a.Name
                FROM book b
                LEFT JOIN category c ON b.CategoryID = c.CategoryID  
                LEFT JOIN author a ON b.AuthorID = a.AuthorID
                WHERE b.BookID IN ({placeholders})
            """, book_ids)
            
            books_info = {}
            for row in cursor.fetchall():
                book_id, category_id, author_id, price, category_name, author_name = row
                books_info[book_id] = {
                    'category_id': category_id,
                    'author_id': author_id,
                    'price': float(price) if price else 0,
                    'category_name': category_name,
                    'author_name': author_name
                }
        
        # Tính trọng số preferences
        category_scores = defaultdict(float)
        author_scores = defaultdict(float)
        price_ranges = []
        
        for book_id, actions in tracking_data.items():
            if book_id not in books_info:
                continue
                
            book_info = books_info[book_id]
            
            # Tính điểm dựa trên hành động (view=1, add_to_cart=3, purchase=5)
            action_weights = {
                'view': 1,
                'add_to_cart': 3, 
                'purchase': 5,
                'click': 1
            }
            
            book_score = 0
            for action, frequency in actions.items():
                weight = action_weights.get(action, 1)
                book_score += frequency * weight
            
            # Cập nhật preferences
            if book_info['category_id']:
                category_scores[book_info['category_id']] += book_score
                
            if book_info['author_id']:
                author_scores[book_info['author_id']] += book_score
                
            if book_info['price'] > 0:
                price_ranges.append(book_info['price'])
        
        # Tính price range preference
        avg_price = sum(price_ranges) / len(price_ranges) if price_ranges else 0
        price_std = 0
        if len(price_ranges) > 1:
            variance = sum((p - avg_price) ** 2 for p in price_ranges) / len(price_ranges)
            price_std = variance ** 0.5
            
        user_profile = {
            'user_id': user_id,
            'preferred_categories': dict(category_scores),
            'preferred_authors': dict(author_scores),
            'price_preference': {
                'avg': avg_price,
                'std': price_std,
                'min': min(price_ranges) if price_ranges else 0,
                'max': max(price_ranges) if price_ranges else 999999
            }
        }
        
        return user_profile
    
    def get_content_based_recommendations(self, user_id, limit=10):
        """Gợi ý sách dựa trên content-based filtering"""
        user_profile = self.build_user_profile(user_id)
        
        if not user_profile:
            # Fallback: gợi ý sách phổ biến
            return self.get_popular_books(limit)
            
        # Lấy sách user chưa tương tác
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT BookID FROM useractivity WHERE CustomerID = %s
            """, [user_id])
            
            interacted_books = {row[0] for row in cursor.fetchall()}
            
            # Lấy tất cả sách có thể gợi ý
            cursor.execute("""
                SELECT b.BookID, b.Title, b.CategoryID, b.AuthorID, b.Price, 
                       b.ImageURL, b.Description, c.CategoryName, a.Name
                FROM book b
                LEFT JOIN category c ON b.CategoryID = c.CategoryID
                LEFT JOIN author a ON b.AuthorID = a.AuthorID  
                WHERE b.Stock > 0
            """)
            
            recommendations = []
            
            for row in cursor.fetchall():
                book_id, title, category_id, author_id, price, image_url, description, category_name, author_name = row
                
                if book_id in interacted_books:
                    continue
                    
                # Tính điểm gợi ý
                score = 0
                
                # Điểm category
                if category_id in user_profile['preferred_categories']:
                    score += user_profile['preferred_categories'][category_id] * 0.4
                    
                # Điểm author
                if author_id in user_profile['preferred_authors']:
                    score += user_profile['preferred_authors'][author_id] * 0.3
                    
                # Điểm price similarity
                price_pref = user_profile['price_preference']
                if price and price_pref['avg'] > 0:
                    price_diff = abs(float(price) - price_pref['avg'])
                    price_score = max(0, 1 - (price_diff / price_pref['avg']))
                    score += price_score * 0.3
                    
                recommendations.append({
                    'book_id': book_id,
                    'title': title,
                    'author': author_name,
                    'price': float(price) if price else 0,
                    'image_url': image_url,
                    'description': description,
                    'category': category_name,
                    'score': score
                })
            
            # Sắp xếp theo điểm và trả về top recommendations
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:limit]
    
    def get_popular_books(self, limit=10):
        """Lấy sách phổ biến làm fallback"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.BookID, b.Title, b.Price, b.ImageURL, b.Description,
                       a.Name, c.CategoryName, COUNT(ua.BookID) as interaction_count
                FROM book b
                LEFT JOIN author a ON b.AuthorID = a.AuthorID
                LEFT JOIN category c ON b.CategoryID = c.CategoryID
                LEFT JOIN useractivity ua ON b.BookID = ua.BookID
                WHERE b.Stock > 0
                GROUP BY b.BookID
                ORDER BY interaction_count DESC, b.BookID
                LIMIT %s
            """, [limit])
            
            popular_books = []
            for row in cursor.fetchall():
                book_id, title, price, image_url, description, author, category, count = row
                popular_books.append({
                    'book_id': book_id,
                    'title': title,
                    'author': author,
                    'price': float(price) if price else 0,
                    'image_url': image_url,
                    'description': description,
                    'category': category,
                    'score': count
                })
                
            return popular_books
    
    def update_user_interactions(self, user_id, book_id, interaction_type):
        """Cập nhật interaction data - được gọi từ tracking"""
        # Cache invalidation - xóa cache user profile để rebuild lần tới
        if hasattr(self, 'user_preferences') and user_id in self.user_preferences:
            del self.user_preferences[user_id]
            
        return True

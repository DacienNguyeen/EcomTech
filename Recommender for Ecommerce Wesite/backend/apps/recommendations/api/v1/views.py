from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import connection
import json

@api_view(['GET'])
@permission_classes([AllowAny])
def test_connection(request):
    """Test API connection"""
    return Response({
        'success': True,
        'message': 'API connected successfully'
    })

class PopularBooksView(APIView):
    """API để lấy sách phổ biến"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                # Lấy sách có nhiều đơn hàng nhất
                cursor.execute("""
                    SELECT b.BookID, b.Title, b.Price, b.ImageURL, b.Description,
                           a.Name, c.CategoryName,
                           COUNT(od.BookID) as order_count
                    FROM book b
                    LEFT JOIN author a ON b.AuthorID = a.AuthorID
                    LEFT JOIN category c ON b.CategoryID = c.CategoryID
                    LEFT JOIN orderdetail od ON b.BookID = od.BookID
                    WHERE b.Stock > 0
                    GROUP BY b.BookID
                    ORDER BY order_count DESC
                    LIMIT 10
                """)
                
                books = []
                for row in cursor.fetchall():
                    books.append({
                        'id': row[0],
                        'title': row[1],
                        'price': float(row[2]) if row[2] else 0,
                        'image_url': row[3],
                        'description': row[4],
                        'author': row[5],
                        'category': row[6],
                        'order_count': row[7]
                    })
                
                return Response({
                    'success': True,
                    'data': books,
                    'message': 'Lấy danh sách sách phổ biến thành công'
                })
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Lỗi khi lấy danh sách sách phổ biến'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRecommendationsView(APIView):
    """API để lấy gợi ý sách cho user cụ thể"""
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        try:
            with connection.cursor() as cursor:
                # Lấy category từ lịch sử mua hàng của user
                cursor.execute("""
                    SELECT DISTINCT b.CategoryID, COUNT(*) as purchase_count
                    FROM orders o
                    JOIN orderdetail od ON o.OrderID = od.OrderID
                    JOIN book b ON od.BookID = b.BookID
                    WHERE o.CustomerID = %s
                    GROUP BY b.CategoryID
                    ORDER BY purchase_count DESC
                    LIMIT 3
                """, [user_id])
                
                preferred_categories = [row[0] for row in cursor.fetchall()]
                
                if preferred_categories:
                    # Gợi ý sách từ các category user thích
                    placeholders = ','.join(['%s'] * len(preferred_categories))
                    cursor.execute(f"""
                        SELECT b.BookID, b.Title, b.Price, b.ImageURL, b.Description,
                               a.Name, c.CategoryName
                        FROM book b
                        LEFT JOIN author a ON b.AuthorID = a.AuthorID
                        LEFT JOIN category c ON b.CategoryID = c.CategoryID
                        WHERE b.CategoryID IN ({placeholders})
                          AND b.Stock > 0
                          AND b.BookID NOT IN (
                              SELECT DISTINCT od.BookID 
                              FROM orders o 
                              JOIN orderdetail od ON o.OrderID = od.OrderID 
                              WHERE o.CustomerID = %s
                          )
                        ORDER BY RAND()
                        LIMIT 10
                    """, preferred_categories + [user_id])
                else:
                    # Nếu user chưa mua gì, gợi ý sách phổ biến
                    cursor.execute("""
                        SELECT b.BookID, b.Title, b.Price, b.ImageURL, b.Description,
                               a.Name, c.CategoryName,
                               COUNT(od.BookID) as order_count
                        FROM book b
                        LEFT JOIN author a ON b.AuthorID = a.AuthorID
                        LEFT JOIN category c ON b.CategoryID = c.CategoryID
                        LEFT JOIN orderdetail od ON b.BookID = od.BookID
                        WHERE b.Stock > 0
                        GROUP BY b.BookID
                        ORDER BY order_count DESC
                        LIMIT 10
                    """)
                
                books = []
                for row in cursor.fetchall():
                    books.append({
                        'id': row[0],
                        'title': row[1],
                        'price': float(row[2]) if row[2] else 0,
                        'image_url': row[3],
                        'description': row[4],
                        'author': row[5],
                        'category': row[6]
                    })
                
                return Response({
                    'success': True,
                    'data': books,
                    'message': f'Lấy gợi ý sách cho user {user_id} thành công'
                })
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'message': 'Lỗi khi lấy gợi ý sách cho user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

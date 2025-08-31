from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
def test_books(request):
    """Test API để lấy danh sách sách"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM book")
            count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT BookID, Title, Price, ImageURL 
                FROM book 
                LIMIT 5
            """)
            
            books = []
            for row in cursor.fetchall():
                books.append({
                    'id': row[0],
                    'title': row[1], 
                    'price': float(row[2]) if row[2] else 0,
                    'image_url': row[3]
                })
            
            return Response({
                'success': True,
                'total_books': count,
                'sample_books': books
            })
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        })

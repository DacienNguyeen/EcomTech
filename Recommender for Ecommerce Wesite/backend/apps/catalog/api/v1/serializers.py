from rest_framework import serializers
from ...models import Book, Author, Category, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['AuthorID', 'AuthorName', 'Biography']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['PublisherID', 'PublisherName', 'Address', 'ContactInfo']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryID', 'CategoryName']  # Removed Description field


class BookSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['BookID', 'Title', 'AuthorID', 'PublisherID', 'CategoryID', 
                  'Price', 'Stock', 'Description', 'PublicationDate', 'image_url']
    
    def get_image_url(self, obj):
        # Tạo URL hình ảnh dựa trên BookID
        return f"http://127.0.0.1:8000/media/book_images/{obj.BookID}.svg"

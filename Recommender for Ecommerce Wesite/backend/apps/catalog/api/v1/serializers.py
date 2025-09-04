from rest_framework import serializers
from ...models import Book, Author, Category, Publisher


def get_absolute_image_url(image_path):
    """Convert relative image path to absolute URL - same as recommendation service"""
    if not image_path:
        return ''
    if image_path.startswith(('http://', 'https://')):
        return image_path
    if image_path.startswith('/'):
        return f"http://127.0.0.1:8000{image_path}"
    return f"http://127.0.0.1:8000/media/{image_path}"


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
        """Use the same image URL logic as recommendation service"""
        return get_absolute_image_url(obj.ImageURL)

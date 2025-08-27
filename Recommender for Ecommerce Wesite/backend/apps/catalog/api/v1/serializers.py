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
        fields = ['CategoryID', 'CategoryName', 'Description']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['BookID', 'Title', 'AuthorID', 'PublisherID', 'CategoryID', 
                  'Price', 'Stock', 'Description', 'PublicationDate']

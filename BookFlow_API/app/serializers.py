from builtins import setattr
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Category, Book, Loan, Review, Wishlist

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_pic']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create profile
        profile, created = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True, source='categories'
    )
    average_rating = serializers.SerializerMethodField()
    isbn = serializers.CharField(write_only=True)
    decrypted_isbn = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'decrypted_isbn',
            'total_copies', 'available_copies',
            'categories', 'category_ids', 'cover_image', 'average_rating'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_decrypted_isbn(self, obj):
        return obj.isbn

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        isbn = validated_data.pop('isbn', None)
        book = Book(**validated_data)
        if isbn:
            book.isbn = isbn
        book.save()
        book.categories.set(categories)
        return book

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        isbn = validated_data.pop('isbn', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if isbn:
            instance.isbn = isbn
        if categories is not None:
            instance.categories.set(categories)
        instance.save()
        return instance
    
class LoanSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Loan
        fields = ['id', 'book', 'user', 'loan_date', 'due_date', 'return_date', 'status']

class WishlistSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    book_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Book.objects.all(), write_only=True, source='books'
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'books', 'book_ids']

    def update(self, instance, validated_data):
        books = validated_data.pop('books', None)
        if books is not None:
            instance.books.set(books)
        instance.save()
        return instance

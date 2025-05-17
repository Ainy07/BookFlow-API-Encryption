from builtins import Exception
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Category, Book, Loan, Review, Wishlist
from .serializers import UserSerializer, UserProfileSerializer, CategorySerializer, BookSerializer, LoanSerializer, ReviewSerializer, WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .utils.encryption import encrypt_data, decrypt_data

from app import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'title', 'isbn', 'categories']
    @action(detail=False, methods=['post'], url_path='encrypt')
    def encrypt_text(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        encrypted = encrypt_data(text)
        return Response({"encrypted": encrypted})
    
    @action(detail=False, methods=['post'], url_path='decrypt')
    def decrypt_text(self, request):
        encrypted_text = request.data.get('encrypted_text')
        if not encrypted_text:
            return Response({"error": "No encrypted_text provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decrypted = decrypt_data(encrypted_text)
        except Exception:
            return Response({"error": "Decryption failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"decrypted": decrypted})
    
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.available_copies < 1:
            raise serializers.ValidationError("No copies available to loan.")
        book.available_copies -= 1
        book.save()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.status != 'ongoing':
            return Response({'error': 'Loan already returned or closed.'}, status=status.HTTP_400_BAD_REQUEST)
        loan.status = 'returned'
        loan.return_date = timezone.now()
        loan.book.available_copies += 1
        loan.book.save()
        loan.save()
        serializer = self.get_serializer(loan)
        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs.get('book_pk')
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_pk')
        serializer.save(user=self.request.user, book_id=book_id)

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_book(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            wishlist.books.add(book)
            return Response({'status': 'book added to wishlist'})
        except Book.DoesNotExist:
            return Response({'error': 'Book not'})

    @action(detail=False, methods=['post'])
    def remove_book(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            wishlist.books.remove(book)
            return Response({'status': 'book removed from wishlist'})
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)
from builtins import Exception, property, round, sum
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from .utils.encryption import encrypt_data, decrypt_data
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn_encrypted = models.TextField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='books')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None

    @property
    def isbn(self):
        try:
            return decrypt_data(self.isbn_encrypted)
        except Exception:
            return None  

    @isbn.setter
    def isbn(self, value):
        self.isbn_encrypted = encrypt_data(value)
        
class Loan(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    book = models.ForeignKey(Book, related_name='loans', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='loans', on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')

    def __str__(self):
        return f"{self.user.username} loaned {self.book.title}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
from django.contrib import admin
from .models import Book, Loan, Category, UserProfile, Review, Wishlist
from django.utils.html import format_html

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available_copies', 'total_copies', 'display_categories')
    search_fields = ('title', 'author')
    list_filter = ('author', 'categories')
    readonly_fields = ('cover_image_preview',)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.cover_image.url)
        return "-"
    cover_image_preview.short_description = 'Cover Image Preview'

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'loan_date', 'due_date', 'return_date', 'status')
    list_filter = ('status',)
    search_fields = ('book__title', 'user__username')
    date_hierarchy = 'loan_date'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'profile_pic_preview')
    search_fields = ('user__username', 'phone', 'address')
    readonly_fields = ('profile_pic_preview',)

    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" style="height: 100px;" />', obj.profile_pic.url)
        return "-"
    profile_pic_preview.short_description = 'Profile Picture Preview'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at')  
    search_fields = ('user__username', 'book__title')

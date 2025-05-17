from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ReviewViewSet, UserViewSet, BookViewSet, LoanViewSet, LoginAPIView, WishlistViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)
router.register('categories', CategoryViewSet)
router.register(r'books/(?P<book_pk>\d+)/reviews', ReviewViewSet, basename='book-reviews')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginAPIView.as_view(), name='login'),
]

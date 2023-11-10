from django.urls import path
from .views import get_profile, add_book, get_books_json, get_reviews_json, visit_profile
app_name = 'Dashboard'

urlpatterns = [
    path('', get_profile, name='get-profile'),
    path('visit/<str:username>/', visit_profile, name='visit-profile'),
    path('add-book/', add_book, name='add_book'),
    path('get-books/', get_books_json, name='get-books'),
    path('get-reviews/', get_reviews_json, name='get-reviews'),
]

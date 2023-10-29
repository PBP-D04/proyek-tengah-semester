from django.urls import path
from .views import home, get_books_json, all_books_page, get_categories, search_category_page,search_page, search_books_json,advanced_search
app_name = 'Homepage'

urlpatterns = [
    path('', home, name='home'),
    path('get-books/', get_books_json, name='get-books' ),
    path('all-books/', all_books_page, name='all-books-page'),
    path('search-books/<str:category>', search_category_page, name='search-category-page'),
    path('search-books/<str:category>/<str:search_text>/', search_page, name='search-page'),
    path('search-books-json/<str:category>/<str:search_text>', search_books_json, name='search-books-json' ),
    path('get-categories/', get_categories, name='get-categories'),
    path('advanced-search-json/', advanced_search, name='advanced-search')
]

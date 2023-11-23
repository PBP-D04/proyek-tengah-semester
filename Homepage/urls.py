from django.urls import path
from .views import home, proxy_endpoint,get_books_json,get_books, all_books_page, get_categories, get_dummy_message, search_page, search_books_json,advanced_search
app_name = 'Homepage'

urlpatterns = [
    path('', home, name='home'),
    path('proxy/<path:target_url>/', proxy_endpoint),
    path('get-books/', get_books, name='get-books' ),
    path('get-books-json/', get_books_json),
    path('all-books/', all_books_page, name='all-books-page'),
    path('search-books/<str:category>/<str:search_text>/', search_page, name='search-page'),
    path('search-books-json/<str:category>/<str:search_text>', search_books_json, name='search-books-json' ),
    path('get-categories/', get_categories, name='get-categories'),
    path('advanced-search-json/', advanced_search, name='advanced-search'),
    path('dummy/', get_dummy_message)
]

from django.urls import path
from .views import home, get_books, all_books_page, get_categories, book_detail, add_comment_ajax, get_comment_json
app_name = 'DetailBook'

urlpatterns = [
    path('', home, name='home'),
    path('get-books/', get_books, name='get-books'),
    path('all-books/', all_books_page, name='all-books-page'),
    path('get-categories/', get_categories, name='get-categories'),
    path('book-detail/<int:id>', book_detail, name='book_detail'),
    path('all-books/book-detail/<int:id>', book_detail, name='book_detail'),
    path('add-comment-ajax/', add_comment_ajax, name='add_comment_ajax'),  
    path('get-comment/<int:book_id>', get_comment_json, name='get_comment_json'),
]

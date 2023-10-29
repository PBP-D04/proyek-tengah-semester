import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from DetailBook.forms import CommentForm
from DetailBook.models import Comment
from Homepage.models import Book, Category
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

def home(request):
    return render(request, "home.html")

def get_books(request):
    return render(request, 'get_books.html')

def all_books_page(request):
    return render(request, "allbooks-page.html")

@csrf_exempt
def get_categories(request):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        categories_list.append(category.name)
    return JsonResponse({'categories':categories_list})


@csrf_exempt
def get_books_json(request):
    books = Book.objects.prefetch_related('authors', 'images', 'categories').all()
    book_list = []
    for book in books:
        book_data  = {
            'title': book.title,
            'subtitle': book.subtitle,
            'description': book.description,
            'authors': [author.name for author in book.authors.all()],
            'publisher': book.publisher,
            'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
            'language': book.language,
            'currencyCode': book.currencyCode,
            'is_ebook': book.is_ebook,
            'pdf_available': book.pdf_available,
            'pdf_link': book.pdf_link,
            'thumbnail': book.thumbnail,
            'categories': [category.name for category in book.categories.all()],
            'images': [imageUrl.url for imageUrl in book.images.all()],
            'price': book.price,
            'saleability': book.saleability,
            'buy_link': book.buy_link,
            'epub_available': book.epub_available,
            'epub_link': book.epub_link,
            'maturity_rating': book.maturity_rating,
            'page_count': book.page_count,
        }
        book_list.append(book_data)
    return JsonResponse({'books': book_list})

@login_required(login_url='/login/') 
def book_detail(request, id):
    book = Book.objects.prefetch_related('authors', 'images', 'categories').get(pk = id)
    book = {
        'pk':book.pk,
        'title': book.title,
        'subtitle': book.subtitle,
        'description': book.description,
        'authors': [author.name for author in book.authors.all()],
        'publisher': book.publisher,
        'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None,
        'language': book.language,
        'currencyCode': book.currencyCode,
        'is_ebook': book.is_ebook,
        'pdf_available': book.pdf_available,
        'pdf_link': book.pdf_link,
        'thumbnail': book.thumbnail,
        'categories': [category.name for category in book.categories.all()],
        'images': [imageUrl.url for imageUrl in book.images.all()],
        'price': book.price,
        'saleability': book.saleability,
        'buy_link': book.buy_link,
        'epub_available': book.epub_available,
        'epub_link': book.epub_link,
        'maturity_rating': book.maturity_rating,
        'page_count': book.page_count,
    }
    book['authors'] = ", ".join(book['authors'])
    book['categories'] = ", ".join(book['categories'])
    comment_form = CommentForm()
    context = {'book': book, 'comment_form': comment_form}
    return render(request, 'book_detail.html', context)


@csrf_exempt
def add_comment_ajax(request):
    data = json.loads(request.body)
    print(data)
    book = Book.objects.prefetch_related('authors', 'images', 'categories').get(pk=data['bookId'])
    print(book)
    if request.method == 'POST':
        
        try:
            new_comment = Comment(content=data['comment'], book=book)
            new_comment.save()
            return JsonResponse({'status':201})
        except Exception as e:
            print(e)
        
    return HttpResponseNotFound()


def get_comment_json(request):
    comment = Comment.objects.all()
    print(comment)
    return HttpResponse(serializers.serialize('json', comment))
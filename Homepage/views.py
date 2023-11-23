import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Book, Category
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from pusher_function import *
import asyncio
import requests

@csrf_exempt  # Hanya untuk tujuan demonstrasi, sebaiknya gunakan cara autentikasi yang aman di produksi
def proxy_endpoint(request, target_url):
    # Dapatkan target_url dari parameter di URL
    final_url = f'https://${target_url}'  # Ubah sesuai kebutuhan

    # Lakukan permintaan ke sumber daya eksternal menggunakan requests library
    response = requests.get(final_url)

    # Ambil konten dari respons dan kirimkan kembali sebagai respons dari endpoint proxy
    return JsonResponse(response.json())


@csrf_exempt
def get_dummy_message(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async_result = loop.run_until_complete(dummy_check_is_ok())
    loop.close()
    return JsonResponse({'status':'OK'})
# Create your views here.
@csrf_exempt
def advanced_search(request):
    search_parameters = json.loads(request.body)
    print(search_parameters)
    query = Q()
    if search_parameters['allWords']:
        words = search_parameters['allWords'].split()
        for word in words:
            query |= Q(title__icontains=word)
    
    if search_parameters['exactPhrase']:
        query &= Q(title__icontains=search_parameters['exactPhrase'])

    if search_parameters['atLeastWords']:
        words = search_parameters['atLeastWords'].split()
        at_least_query = Q()  # Query Q untuk at least words
        for word in words:
            at_least_query |= Q(title__icontains=word)
        query &= at_least_query

    if search_parameters['withoutWords']:
        words = search_parameters['withoutWords'].split()
        without_query = Q()  # Query Q untuk without words
        for word in words:
            without_query &= ~Q(title__icontains=word)
        query &= without_query

    books = Book.objects.prefetch_related('authors', 'images', 'categories').filter(query)
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
            'images':[imageUrl.url for imageUrl in book.images.all()],
            'price': book.price,
            'saleability': book.saleability,
            'buy_link': book.buy_link,
            'epub_available': book.epub_available,
            'epub_link': book.epub_link,
            'maturity_rating': book.maturity_rating,
            'page_count': book.page_count,
            'user_publish_time': book.user_publish_time
        }
        book_list.append(book_data)
    return JsonResponse({'books': book_list})

def home(request):
    print(request.user.is_authenticated)
    context = {
        
    }
    return render(request, "home.html")

def all_books_page(request):
    return render(request, "allbooks-page.html")

@csrf_exempt
def get_categories(request):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        categories_list.append(category.name)
    return JsonResponse({'categories':categories_list})
def search_page(request, category, search_text ):
    information = {
        'category':category,
        'search_text':search_text
    }
    return render(request,'search-page.html', information)

@csrf_exempt
def search_books_json(request, category, search_text):
    books = []
    if(category == 'All'):
        books  = Book.objects.prefetch_related('authors', 'images', 'categories').filter(
        title__icontains=search_text.strip())
    else:
        books  = Book.objects.prefetch_related('authors', 'images', 'categories').filter(
        title__icontains=search_text, categories__name=category)
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
            'images':[imageUrl.url for imageUrl in book.images.all()],
            'price': book.price,
            'saleability': book.saleability,
            'buy_link': book.buy_link,
            'epub_available': book.epub_available,
            'epub_link': book.epub_link,
            'maturity_rating': book.maturity_rating,
            'page_count': book.page_count,
            'user_publish_time': book.user_publish_time
        }
        book_list.append(book_data)

    return JsonResponse({'books': book_list})

@csrf_exempt
def get_books(request):
    books  = Book.objects.prefetch_related('authors', 'images', 'categories').all()
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
            'images':[imageUrl.url for imageUrl in book.images.all()],
            'price': book.price,
            'saleability': book.saleability,
            'buy_link': book.buy_link,
            'epub_available': book.epub_available,
            'epub_link': book.epub_link,
            'maturity_rating': book.maturity_rating,
            'page_count': book.page_count,
            'user_publish_time': book.user_publish_time
        }
        book_list.append(book_data)

    return JsonResponse({'books': book_list})
@csrf_exempt
def get_books_json(request):
    books = Book.objects.prefetch_related('authors', 'images', 'categories', 'user_like', 'review_book__user__auth_user').select_related('user__auth_user').all()
    book_list = []
    for book in books:
        book_data  = {
            'review': [review.to_dict() for review in book.review_book.all()],
            'user': book.user.auth_user.to_dict(),
            'book': {
                'id': book.pk,
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
                'images':[imageUrl.url for imageUrl in book.images.all()],
                'price': book.price,
                'saleability': book.saleability,
                'buy_link': book.buy_link,
                'epub_available': book.epub_available,
                'epub_link': book.epub_link,
                'maturity_rating': book.maturity_rating,
                'page_count': book.page_count,
                'user_publish_time': book.user_publish_time,
                'book_likes':[{'username': user.username, 'userId': user.pk} for user in book.user_like.all()]
            }
        }
        
        book_list.append(book_data)
    return JsonResponse({'book_list': book_list})
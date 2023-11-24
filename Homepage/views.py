import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Book, Category
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from pusher_function import *
import asyncio
import requests
import urllib3
from Bookphoria.models import Like
from django.contrib.auth.models import User

@csrf_exempt
def proxy_endpoint(request, target_url):
    http = urllib3.PoolManager()

    final_url = f'https://{target_url}'  # Ubah sesuai kebutuhan, misalnya: 'https://{target_url}'

    try:
        response = http.request('GET', final_url)

        # Mendapatkan status code dari respons
        status_code = response.status

        # Mendapatkan tipe konten gambar
        content_type = response.headers.get('Content-Type', 'application/octet-stream')

        # Mendapatkan konten gambar
        image = response.data

        # Return response dalam bentuk HttpResponse
        return HttpResponse(image, content_type=content_type, status=status_code)
    except urllib3.exceptions.HTTPError as e:
        # Tangani kesalahan permintaan HTTP
        return HttpResponse(f'HTTP error occurred: {e}', status=500)
    except Exception as e:
        # Tangani kesalahan umum lainnya
        return HttpResponse(f'An error occurred: {e}', status=500)

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
def like_or_dislike_book(request):
    if request.method == 'POST':
        print('KUAKUUIIIIIIIIIIIIIIIIIIIIIIIIIIII........................')
        data = json.loads(request.body)
        bookId = data['bookId']
        userId = data['userId']
        is_liked = True
        try:
            book = Book.objects.prefetch_related('user_like').get(pk=bookId)
            print('LELET BANGET DJANGOOOOOOOOOOOOOOOOOO')
            if(book is None):
                return JsonResponse({'message': 'Buku sudah dihapus', 'status': 404})
            like_exists = book.user_like.filter(user_id=userId)
            if like_exists.exists():
                like_exists.delete()
                is_liked = False
            else:
                like = Like.create_like_with_id(user_id=userId, book_id=bookId)
                book.user_like.add(like)
            update_book_like(book_id=bookId, user_id=userId, is_liked=is_liked) #FUNGSI KE PUSHER
            return JsonResponse({'message': 'Buku berhasil diperbarui', 'status': 200})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User tidak ada', 'status': 404})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Buku tidak ada', 'status': 404})
    return JsonResponse({'message': 'Kesalahan pengiriman formulir', 'status': 500})

# UDAH PALING GACOR, PAKAI INI UNTUK AMBIL DATA BUKU DARI DJANGO
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
                'user_publish_time': book.user_publish_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'book_likes':[like.to_dict() for like in book.user_like.all()]
            }
        }
        
        book_list.append(book_data)
    return JsonResponse({'book_list': book_list})
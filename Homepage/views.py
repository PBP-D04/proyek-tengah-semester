import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Book, Category
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from Bookphoria.models import UserProfile

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
        profil = Profil.objects.get(user=book.user)
        book_data  = {
            'fullname':profil.fullname,
            'username':profil.username,
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
        'search_text':search_text,
        'is_category_only':"False"
    }
    return render(request,'search-page.html', information)
def search_category_page(request,category):
    information = {
        'category':category,
        'search_text':'',
        'is_category_only':"True"
    }
    return render(request, 'search-page.html', information)

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

def search_books_json_category(request, category):
    books = []
    if(category == 'All'):
        books  = Book.objects.prefetch_related('authors', 'images', 'categories').all()
    else:
        books  = Book.objects.prefetch_related('authors', 'images', 'categories').filter(categories__name=category)
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
    books = Book.objects.prefetch_related('authors', 'images', 'categories').select_related('user__auth_user').all()
    book_list = []
    for book in books:
        book_data  = {
            'fullname':book.user.auth_user.fullname,
            'username':book.user.auth_user.username,
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
        }
        book_list.append(book_data)
    return JsonResponse({'books': book_list})
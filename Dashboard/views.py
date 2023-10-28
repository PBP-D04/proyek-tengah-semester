from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from Dashboard.forms import BookForm
from Homepage.models import Book, Author, Category
from Bookphoria.models import Review

@login_required
def get_profile(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_book(request)
        return HttpResponseRedirect(reverse('Dashboard:get-profile'))
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
        book_list.append(book.thumbnail)
        # print(book.thumbnail)
        # print(book_list)
    context = {
        'books':book_list,
        'form': form
    }
    return render(request, 'profile.html', context)

@csrf_exempt
def add_book(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_book = form.save(commit=False)
        new_book.user = request.user

        new_book.save()

        print(Book.objects.filter(user=new_book.user).prefetch_related('authors', 'images', 'categories'))  
        return HttpResponse(b"CREATED", status=201)

    context = {'form': form}
    print("=======================NICE COKC=====================")
    return render(request, 'add_book.html', context)

@csrf_exempt
def get_books_json(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden()
    print(user)
    books = Book.objects.filter(user=user).prefetch_related('authors', 'images', 'categories')
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
            'user_publish_time': book.user_publish_time,
        }
        book_list.append(book_data)
    return JsonResponse({'books': book_list})

@csrf_exempt
def get_reviews_json(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden()
    print(user)
    reviews = Review.objects.filter(user=user)
    review_list = []
    for review in reviews:
        review_data  = {
            'thumbnail': review.thumbnail,
            'title': review.title,
            'rating': review.rating,
            'content': review.content,
        }
        review_list.append(review_data)
    return JsonResponse({'reviews': review_list})
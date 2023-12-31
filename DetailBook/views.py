import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from DetailBook.forms import CommentForm
from DetailBook.models import Comment, CommentV2
from Homepage.models import Book, Category
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
from pusher_function import realtime_update_comment

def coba_coba_komen(request):
    data = {
        'user_id':1,
        'book_id':1,
        'content':'Ada yang punya rekomendasi buku yang sama dengan ini?'
    }
    comment = CommentV2.create_with_id(user_id=data['user_id'],book_id=data['book_id'], content=data['content'])
    commentToSend = CommentV2.objects.select_related('user__auth_user').get(pk=comment.pk)
    realtime_update_comment(comment= commentToSend.to_dict())
    return JsonResponse({
        'status':200,
        'message':'Berhasil menambahkan Komentar'
    })

@csrf_exempt
def add_comment_v2(request):
    data = json.loads(request.body)
    comment = CommentV2.create_with_id(user_id=data['user_id'],book_id=data['book_id'], content=data['content'])
    commentToSend = CommentV2.objects.select_related('user__auth_user').get(pk=comment.pk)
    realtime_update_comment(comment= commentToSend.to_dict())
    return JsonResponse({
        'status':200,
        'message':'Berhasil menambahkan Komentar'
    })

@csrf_exempt
def get_all_comment_v2(request):
    comments = CommentV2.objects.select_related('user__auth_user').all()
    commentList = []
    for comment in comments:
        commentList.append(comment.to_dict())
    return JsonResponse({'commentList': commentList, 'status':200, })


    

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


def get_comment_json(request, book_id):
    comments = Comment.objects.filter(book__id=book_id)
    return HttpResponse(serializers.serialize('json', comments), content_type="application/json")
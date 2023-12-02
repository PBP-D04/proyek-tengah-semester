from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from Bookphoria.models import UserProfile
from Dashboard.forms import BookForm
from Homepage.models import Book, Author, Category, ImageUrl
from pusher_function import realtime_delete_book,create_new_book
#from Bookphoria.models import Review
from ReviewApp.models import Review
import json
from faker import Faker

@csrf_exempt
def delete_books(request):
    data = json.loads(request.body)
    lst = Book.delete_from_json(data)
    realtime_delete_book(lst=lst)
    return JsonResponse({'message':'sukses menghapus buku', 'status':200})


def create_random_book(request):
    if request.method == 'GET':
        try:
            fake = Faker()

            # Dapatkan data buku acak
            book_data = {
                'user_id': 1,
                'title': fake.sentence(nb_words=4),
                'subtitle': fake.sentence(nb_words=6),
                'description': fake.paragraph(nb_sentences=5),
                'publisher': fake.company(),
                'published_date': '2004-04-04',
                'language': fake.language_code(),
                'currency_code': 'IDR',
                'is_ebook': fake.boolean(),
                 'images' : [fake.image_url() for _ in range(4)],
                 'categories' : [fake.word() for _ in range(2)],
                'pdf_available': fake.boolean(),
                'pdf_link': fake.uri() if fake.boolean(chance_of_getting_true=30) else None,
                'thumbnail': fake.image_url(),
                'price': '14000',
                'saleability': fake.boolean(),
                'buy_link': fake.uri() if fake.boolean(chance_of_getting_true=30) else None,
                'epub_available': fake.boolean(),
                'epub_link': fake.uri() if fake.boolean(chance_of_getting_true=30) else None,
                'maturity_rating': fake.random_element(elements=['NOT_MATURE', 'MATURE']),
                'page_count': fake.random_int(50, 500),
                #'user_publish_time': timezone.now(),
                'authors' :[fake.name() for _ in range(2)]
                # Tambahkan atribut lainnya dari Faker sesuai kebutuhan
            }

            # Buat buku baru dari data yang diterima
            new_book = Book.create_from_json(book_data)

            # Berhasil membuat buku acak
            return JsonResponse({'message': 'Successfully created random book', 'book_id': new_book.id}, status=201)
        except Exception as e:
            # Jika terjadi kesalahan, kirimkan pesan kesalahan
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@csrf_exempt
def edit_book_flutter(request):
    data = json.loads(request.body)
    print(data)
    bookId = data['book_id']
    book = Book.objects.get(pk=bookId)
    book.images.clear()
    book.authors.clear()
    book.categories.clear()
    book_json = data
    #book.user_id=book_json['user_id'],
    book.title=book_json['title']
    print('MANA SIH CUK 1')
    book.subtitle=book_json['subtitle']
    book.description=book_json['description']
    book.publisher=book_json['publisher']
    book.published_date=datetime.strptime(book_json['published_date'], '%Y-%m-%dT%H:%M:%S.%f') if book_json['published_date'] else None
    book.language=book_json['language']
    print('MANA SIH CUK 2')
    book.currencyCode=book_json['currency_code']
    book.is_ebook=book_json['is_ebook']
    book.pdf_available=book_json['pdf_available']
    book.pdf_link=book_json.get('pdf_link')
    book.thumbnail=book_json.get('thumbnail')
    book.price=book_json.get('price')
    print('MANA SIH CUK 3')
    book.saleability=book_json.get('saleability', False)
    book.buy_link=book_json.get('buy_link')
    book.epub_available=book_json.get('epub_available', False)
    book.epub_link=book_json.get('epub_link')
    book.maturity_rating=book_json['maturity_rating']
    print('MANA SIH CUK 4')
    book.page_count=book_json['page_count']
    book.save()
    authors_list = book_json.get('authors', [])
    for author_name in authors_list:
            # Mencari penulis berdasarkan nama atau membuat penulis baru jika tidak ada
        author, created = Author.objects.get_or_create(name=author_name)
        book.authors.add(author)
    images = book_json.get('images',[])
    for img_url in images:
        image = ImageUrl.objects.create(url=img_url)
        book.images.add(image)
    categories_name = book_json.get('categories',[])
    for category_name in categories_name:
        category, created = Category.objects.get_or_create(name=category_name)
        book.categories.add(category)
    book = Book.objects.prefetch_related('authors', 'images', 'categories', 'user_like', 'review_book_v2__user__auth_user').select_related('user__auth_user').get(pk=book.pk)
    book_data  = {
            'review': [review.to_dict() for review in book.review_book_v2.all()],
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
                'user_publish_time': (book.user_publish_time).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'book_likes':[like.to_dict() for like in book.user_like.all()]
            }
    }
    create_new_book(book_data=book_data)
    return JsonResponse({'message': 'Successfully created  book', 'book_id': book.id}, status=201)


@csrf_exempt
def create_book_flutter(request):
    data = json.loads(request.body)
    new_book = Book.create_from_json(data)
    book = Book.objects.prefetch_related('authors', 'images', 'categories', 'user_like', 'review_book_v2__user__auth_user').select_related('user__auth_user').get(pk=new_book.pk)
    book_data  = {
            'review': [review.to_dict() for review in book.review_book_v2.all()],
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
                'user_publish_time': (book.user_publish_time).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'book_likes':[like.to_dict() for like in book.user_like.all()]
            }
    }
    create_new_book(book_data=book_data)
            
    return JsonResponse({'message': 'Successfully created  book', 'book_id': new_book.id}, status=201)

@login_required(login_url='/login/')
def get_profile(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_book(request)
        return HttpResponseRedirect(reverse('Dashboard:get-profile'))
    books = Book.objects.prefetch_related('authors', 'images', 'categories').all()
    book_list = []
    user = UserProfile.objects.get(user=request.user)
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
    if user.profile_picture is None:
        user.profile_picture = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ03Q9ChkabFQ9M3syb-NEQOk9x34zv4pfFQ&usqp=CAU'
    context = {
        'books':book_list,
        'form': form,
        'user': user
    }
    return render(request, 'profile.html', context)

def visit_profile(request, username):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_book(request)
        return HttpResponseRedirect(reverse('Dashboard:get-profile'))
    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return render(request, 'user-not-exist.html')
    books = Book.objects.prefetch_related('authors', 'images', 'categories').all()
    book_list = []
    user = UserProfile.objects.get(username=username)
    print("=====================================")
    print(user)
    print("=====================================")
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
    if user.profile_picture is None:
        user.profile_picture = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ03Q9ChkabFQ9M3syb-NEQOk9x34zv4pfFQ&usqp=CAU'
    context = {
        'books':book_list,
        'form': form,
        'user': user
    }
    return render(request, 'visit-profile.html', context)

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
           # 'thumbnail': review.thumbnail,
            'thumbnail' : review.photo.url if review.photo else "https://m.media-amazon.com/images/I/71lgQcXtPMS._AC_UF894,1000_QL80_.jpg",
            'title': "Sebuah Judul" if review.book.title is None else review.book.title,  # Review dr Review App ga include title
            'rating': review.rating,
            'content': review.content,
        }
        review_list.append(review_data)
    return JsonResponse({'reviews': review_list})
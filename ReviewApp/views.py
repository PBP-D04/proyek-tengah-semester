import datetime
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseNotFound

from Homepage.models import Book
from .models import Review, ReviewV2
from .forms import ReviewForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.contrib.auth.decorators import login_required
from pusher_function import realtime_update_review, realtime_delete_review


def coba_coba_review(request):
    data = {
        'user_id':1,
        'book_id':80,
        'rating':5,
        'content': 'Buku ini sangat menarik untuk dibaca oleh semua kalangan',
        'photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKazETeZCBVzGuEHvbfRheh5zg1Q38fp4blA&usqp=CAU'
    }
    review = ReviewV2.create_with_id(user_id=data['user_id'], rating= data['rating'],
                            book_id=data['book_id'], content=data['content'], photo= data['photo'])
    review_to_send = Review.objects.select_related('user__auth_user').get(pk=review.pk)
    realtime_update_review(review=review_to_send.to_dict())
    return JsonResponse({'message':'berhasil menambahkan review', 'status':200})

@csrf_exempt
def update_review_flutter(request):
    data = json.loads(request.body)
    review = ReviewV2.objects.select_related('user__auth_user').get(pk=data['review_id'])
    review.content = data['content']
    review.rating = data['rating']
    review.photo = data['photo']
    review.save(force_update=True)
    realtime_update_review(review=review.to_dict())
    return JsonResponse({'message':'berhasil mengedit review', 'status':200})

# Create your views here.
@csrf_exempt
def add_review_flutter(request):
    data = json.loads(request.body)
    review = ReviewV2.create_with_id(user_id=data['user_id'], rating= data['rating'],
                            book_id=data['book_id'], content=data['content'], photo= data['photo'])
    review_to_send = ReviewV2.objects.select_related('user__auth_user').get(pk=review.pk)
    realtime_update_review(review=review_to_send.to_dict())
    return JsonResponse({'message':'berhasil menambahkan review', 'status':200})

@csrf_exempt
def delete_review_flutter(request):
    data = json.loads(request.body)
    reviewData = ReviewV2.objects.get(pk=data['review_id'])
    idToDelete = reviewData.pk
    reviewData.delete()
    realtime_delete_review(idToDelete)
    return JsonResponse({'message':'berhasil menambahkan review', 'status':200})

@csrf_exempt
def get_review_flutter(request):
    reviews = ReviewV2.objects.select_related('user__auth_user').all()
    review_list = []
    for review in reviews:
        review_list.append(review.to_dict())
    return JsonResponse({'reviews': review_list, 'status': 200})


def home(request):
    return render(request, "home.html")

@csrf_exempt
def get_review_json(request):
    reviews = Review.objects.all()
    review_list = []
    for review in reviews:
        review_data  = {
            'user': review.user.username,
            'book': review.book.title,
            'rating': review.rating,
            'content': review.content,
        }
        review_list.append(review_data)
    print("==============KINGDOM ALL==============")
    print(review_list)
    return JsonResponse({'reviews': review_list})

@login_required(login_url='/login/')
def show_review(request):
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        create_review(request)
        return HttpResponseRedirect(reverse('ReviewApp:show_review'))
    bookId = 1
    print("==============KINGDOM BOOK==============")
    print(bookId)
    reviews = Review.objects.all()
    context = {
        'name' : request.user.username,
        'reviews' : reviews,
        'form': form,
    }
    return render(request, 'review.html', context)

# def create_review(request):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST or None)
#         if form.is_valid() and request.method == "POST":
#             review = form.save(commit=False)
#             review.user = request.user
#             review.save()
#             return HttpResponseRedirect(reverse('ReviewApp:show_review'))
#     else:
#         form = ReviewForm()
#         context = {'form': form }
#     return render(request, "book_detail.html", context)

@csrf_exempt
def create_review(request):
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_review = form.save(commit=False)
        new_review.user = request.user
        bookId = int(request.POST.get('book'))
        print("==============KINGDOM COME==============")
        print(new_review)
        new_review.save()

        return JsonResponse({"message": "Product created successfully."}, status=201)

    context = {'form': form}
    return render(request, 'review.html', context)
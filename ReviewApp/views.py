import datetime
import json
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from Homepage.models import Book
from .models import Review
from .forms import ReviewForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.contrib.auth.decorators import login_required


# Create your views here.

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

# @csrf_exempt
# def create_review(request):
#     form = ReviewForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         new_review = form.save(commit=False)
#         new_review.user = request.user
#         bookId = int(request.POST.get('book'))
#         print("==============KINGDOM COME==============")
#         print(new_review)
#         new_review.save()

#         return JsonResponse({"message": "Product created successfully."}, status=201)

#     context = {'form': form}
#     return render(request, 'review.html', context)

@csrf_exempt
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return JsonResponse(model_to_dict(new_review), status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return HttpResponseNotAllowed(['POST'])
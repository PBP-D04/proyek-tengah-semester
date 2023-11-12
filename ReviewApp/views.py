import datetime
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from Homepage.models import Book
from .models import Review, CustomJSONEncoder
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
            'photo': review.photo.url if review.photo else None,
        }
        review_list.append(review_data)
    print("==============KINGDOM ALL==============")
    print(review_list)
    return JsonResponse({'reviews': review_list}, encoder=CustomJSONEncoder)


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


@login_required(login_url='/login/')
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
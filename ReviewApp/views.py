import datetime
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from .models import Review, Book
from .forms import ReviewForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, "home.html")

# def show_review(request):
#     reviews = Review.objects.filter(user=request.user)
#     context = {
#         'name' : request.user.username,
#         'reviews' : reviews,
#     }

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

def get_review_json(request):
    review = Review.objects.all()
    return HttpResponse(serializers.serialize('json', review))

@csrf_exempt
@login_required(login_url='/login/')
def create_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book = Book.objects.prefetch_related('authors', 'images', 'categories').get(pk=data['bookId'])
        rating = data['rating']
        content = data['content']
        photo = data['photo']
        user = request.user

        new_review = Review(book=book, rating=rating, content=content, photo=photo, user=user)
        new_review.save()

        return JsonResponse({"message": "Product created successfully."}, status=201)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
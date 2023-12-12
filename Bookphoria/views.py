import datetime
from django import forms
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
#from Bookphoria.forms import ReviewForm
from django.http import HttpResponse
from django.core import serializers
from django.urls import path, reverse
#from Bookphoria.models import EditProfileForm, Review, UserProfile, UserProfileForm
from Bookphoria.models import EditProfileForm, UserProfile, UserProfileForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
#from Bookphoria.models import Review
#from Bookphoria.forms import ReviewForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from ReviewApp.models import Review # connect to ReviewApp
from django.core.files.storage import default_storage


import json


from Homepage.models import Book

@csrf_exempt
def register(request):
    form = UserProfileForm()
    profile_picture = forms.ImageField(required=False)
    if request.method == "POST":
        username= request.POST['username']
        fullname = request.POST['fullname']
        profile_picture= request.POST['profile_picture']
        age =int(request.POST['age'])
        country = request.POST['country']
        city = request.POST['city']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']#validasi password

        if password1 != password2:
            error_message = "Password yang dimasukkan tidak cocok. Silakan coba lagi."
            return form
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        registered = True
        user_profile = UserProfile(user=user,fullname = fullname,profile_picture=profile_picture, username=username, age=age, country=country, city=city, phone_number=phone_number, password= password1)
        user_profile.save() 
        messages.success(request, 'Your account has been successfully created!')
        return redirect('/login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user_mobile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Proses autentikasi pengguna berdasarkan data yang diterima
            # Contoh autentikasi (harap sesuaikan dengan logika autentikasi yang sesuai)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                return JsonResponse({'message': 'User  tidak ditemukan', 'status': 404})

            # Lakukan verifikasi pengguna di sini (contoh sederhana)
            if user is not None:
                # Jika autentikasi berhasil, kembalikan respons JSON
                user = User.objects.select_related('auth_user').get(username=user.username)
                return JsonResponse({'message': 'Login successful','user': user.auth_user.to_dict(), 'status':200})
            else:
                return JsonResponse({'message': 'Invalid credentials', 'status':401})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def register_user_mobile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            fullname = data.get('fullname')
            profile_picture = data.get('profile_picture')
            age = data.get('age')
            country = data.get('country')
            city = data.get('city')
            phone_number = data.get('phone_number')
            password = data.get('password')
            password_confirm = data.get('password_confirm') 
            print('password->')
            print(password)
            print('ULALAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA') #validasi password
            if password != password_confirm:
                error_message = "Password yang dimasukkan tidak cocok. Silakan coba lagi."
                return JsonResponse({'message': error_message, 'status': 400})
            user = User.objects.create_user(username=username, password=password)
            user.save()
            print('HOLY SHITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT JANGAN ERROR TTTTTTTTTTTTTTTTTT')
            print(password)
           # if 'profile_picture' in request.FILES:
             #   print('found it')
             #   user.profile_picture=request.FILES['profile_picture']
         #   user.save()
            user_profile = UserProfile(user=user,
            fullname=fullname,profile_picture=profile_picture,
            username=username, age=age, country=country, city=city, 
            phone_number=phone_number, password= password)
            user_profile.save() 
            print('HOLY SHITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT JANGAN ERROR 2 TTTTTTTTTTTTTTTTTT')
            return JsonResponse({'message': 'Your account has been successfully created!', 'status': 200})
        except json.JSONDecodeError as e:
            print(e)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("Homepage:home")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response

def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm()
    return render(request, 'user.html', {'form': form})

@login_required(login_url='/login/')
def view_profile(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    print(userProfile.country)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'user.html', {'form': form, 'userProfile':userProfile})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'user.html', {'reviews': reviews})

#def add_review(request, product_id):
   # if request.method == 'POST':
     #   form = ReviewForm(request.POST)
  #      if form.is_valid():
  #          rating = form.cleaned_data['rating']
  #          text = form.cleaned_data['text']
  #          book = Book.objects.get(pk=product_id)  # Gantilah Product dengan model yang sesuai

            # Simpan review ke basis data
    #        review = Review(user=request.user, product=book, rating=rating, text=text)
     #       review.save()
   #         return redirect('review_list')  # Redirect ke halaman daftar review
 #   else:
  #      form = ReviewForm()

   # return render(request, 'user.html', {'form': form})

@csrf_exempt
def edit_profile(request):
    print(request.user)
    form = EditProfileForm(instance=request.user)
    if (request.method == 'POST'):
        fullname = request.POST.get('fullname')
        age = request.POST.get('age')
        country = request.POST.get('country')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        password= request.POST.get('password1')
        userProfile = UserProfile.objects.get(user=request.user)
        userProfile.fullname = fullname
        userProfile.age = age
        userProfile.country= country
        userProfile.city = city
        userProfile.phone_number= phone_number
        userProfile.password = password
        request.user.set_password(password)
        request.user.save()
        userProfile.save()
        user = authenticate(request, username= userProfile.username, password=password)
        if user:
            login(request,user)
            return redirect ('/view/')
        
    userProfile = UserProfile.objects.get(user=request.user)
    return render(request, 'edituser.html', {'form': form, 'userProfile':userProfile})

@csrf_exempt
def edit_profilejson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        userId = data['id']
        userProfile = UserProfile.objects.get(pk=userId)
        userProfile.fullname = data['fullname']
        userProfile.age = data['age']
        userProfile.country= data['country']
        userProfile.city = data['city']
        userProfile.phone_number= data ['phoneNumber']
        confirmPass = data['password']
        if confirmPass != userProfile.password:
            error_message = "Password yang dimasukkan tidak cocok. Silakan coba lagi."
            return JsonResponse(status=400, data={'message': error_message, 'status': 400})
        userProfile.save()
        return JsonResponse(status=200, data={'message': 'Your account has been successfully updated!', 'status': 200})
    return JsonResponse(status=405, data={'error': 'Invalid request method'})

@csrf_exempt
def get_profilejson(request, id):
    userProfile = UserProfile.objects.get(pk=id)
    return JsonResponse(userProfile.to_dict())

@csrf_exempt
def get_previous_edit_data_json(request):
    data = json.loads(request.body)
    print(data)
    userId = data['id']
    userProfile = UserProfile.objects.get(pk=userId)
    userProfileData = {
        'username': userProfile.username,
        'password': userProfile.password,
        'fullname': userProfile.fullname,
        'age': userProfile.age,
        'country': userProfile.country,
        'city': userProfile.city,
        'phoneNumber':userProfile.phone_number

    }
    return JsonResponse(userProfileData)



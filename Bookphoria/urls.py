"""
URL configuration for Bookphoria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from Bookphoria.views import register, get_previous_edit_data_json, edit_profilejson
from Bookphoria.views import login_user 
from Bookphoria.views import logout_user
from django.urls import path
from Bookphoria.models import Like
from Bookphoria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('review_list/', views.review_list, name='review_list'),
    #path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('likes/<int:product_id>/', Like, name='like_book'),
    path('create/', views.create_profile, name='create_profile'),
    path('view/', views.view_profile, name='view_profile'),  
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile_data_json/',get_previous_edit_data_json, name="edit_data_json"),
    path('edit_profilejson/', edit_profilejson, name='edit_profilejson'),
    path('', include('Homepage.urls')),
    path('profile/', include('Dashboard.urls')),
    path('detail/', include('DetailBook.urls')), 
    path('review/', include('ReviewApp.urls')),
]
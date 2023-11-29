from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_user')
    username = models.CharField(max_length=255)
    fullname= models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    password = models.CharField(max_length = 255, blank=False, null =False)

    def to_dict(self):
        return {
            'id':self.user.id,
            'username': self.username,
            'fullname': self.fullname,
            'country':self.country,
            'city':self.city,
            'age':self.age,
            'phone_number':self.phone_number,
            'profile_picture':self.profile_picture
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        profile_picture = forms.ImageField(required=False)
        model = UserProfile
        fields =  ['username',  'fullname', 'password','profile_picture', 'age','phone_number',  'country', 'city' ]

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =  ['username','fullname', 'password','profile_picture', 'age','phone_number',  'country', 'city']

#class Review(models.Model):
  #  user = models.ForeignKey(User, on_delete=models.CASCADE)
 #   thumbnail = models.URLField(blank=True, null=True)
   # title = models.CharField(max_length=255)
   # rating = models.IntegerField(default=5,
     #   validators=[MinValueValidator(0), MaxValueValidator(5)]
  #  )
  #  photo = models.ImageField(upload_to='review_photos/', blank=True, null=True) # add this
  #  content = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True)
   # date_added = models.DateField(auto_now_add=True)
   # date_added = models.DateField(default=timezone.now)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_book = models.ForeignKey('Homepage.Book', on_delete=models.CASCADE, related_name='user_like')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_like_with_id(cls, user_id, book_id):
        like = cls(user_id=user_id, liked_book_id=book_id)
        like.save()
        return like
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'liked_book_id': self.liked_book.id,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            # Tambahkan attribut lainnya jika diperlukan
        }

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

#class ReviewForm(forms.Form):
   # rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)
   # text = forms.CharField(label='Review', widget=forms.Textarea)

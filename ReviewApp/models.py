from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User  # sesuaikan dengan variabel
from Homepage.models import Book


# Create your models here.
#class Author(models.Model):
 #   name = models.CharField(max_length=100)
  #  def __str__(self):
   #     return self.name

#class ImageUrl (models.Model):
  #  url = models.URLField()
   # def __str__(self):
    #    return self.url

#class Category(models.Model):
 #   name = models.CharField(max_length=50)
  #  def __str__(self):
   #     return self.name




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
   # content = models.TextField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
  #  rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating = models.IntegerField(default=5,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    photo = models.ImageField(upload_to='review_photos/', blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)
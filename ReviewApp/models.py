from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User  # sesuaikan dengan variabel
from Homepage.models import Book


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ImageUrl (models.Model):
    url = models.URLField()
    def __str__(self):
        return self.url

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    subtitle = models.CharField(max_length=255, blank=True, null=True )
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField('Author', related_name='authors_book')  
    publisher = models.CharField(max_length=100, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=10)
    currencyCode= models.CharField(max_length=10, blank=True, null=True)
    is_ebook = models.BooleanField()
    pdf_available = models.BooleanField()
    pdf_link = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    images = models.ManyToManyField(ImageUrl)
    categories = models.ManyToManyField('Category',  related_name='book_categories')
    price = models.CharField(max_length=255, blank=True, null=True)
    saleability = models.BooleanField(default=False)
    buy_link = models.URLField(blank=True, null=True)
    epub_available = models.BooleanField(default=False)
    epub_link = models.URLField(blank=True, null=True)
    maturity_rating = models.CharField(max_length=25)
    page_count = models.IntegerField(default=1,
        validators=[MinValueValidator(1)]
    )
    user_publish_time = models.DateTimeField(blank=True, null=True, default= timezone.now)
    user_last_edit_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(max_length=255, blank=True, null=True)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    image = models.ImageField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from Bookphoria.models import Like
import datetime
import pytz
from datetime import date,datetime,timedelta


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    subtitle = models.CharField(max_length=255, blank=True, null=True )
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField('Author', related_name='authors_book')  
    publisher = models.CharField(max_length=100, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=10)
    currencyCode = models.CharField(max_length=10, blank=True, null=True)
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
    user_publish_time = models.DateTimeField(auto_now_add=True)
    user_last_edit_time = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes_book')

    @classmethod
    def delete_from_json(cls, lst_json):
        Book.objects.filter(id__in=lst_json['books']).delete()
        return lst_json['books']

    @classmethod
    def create_from_json(cls, book_json):
        new_book = cls(
            user_id=book_json['user_id'],
            title=book_json['title'],
            subtitle=book_json['subtitle'],
            description=book_json['description'],
            publisher=book_json['publisher'],
            published_date=datetime.strptime(book_json['published_date'], '%Y-%m-%dT%H:%M:%S.%f') if book_json['published_date'] else None,
            language=book_json['language'],
            currencyCode=book_json.get('currency_code', 'ID'),
            is_ebook=book_json['is_ebook'],
            pdf_available=book_json['pdf_available'],
            pdf_link=book_json.get('pdf_link'),
            thumbnail=book_json.get('thumbnail'),
            price=book_json.get('price'),
            saleability=book_json.get('saleability', False),
            buy_link=book_json.get('buy_link'),
            epub_available=book_json.get('epub_available', False),
            epub_link=book_json.get('epub_link'),
            maturity_rating=book_json.get('maturity_rating', 'NOT_MATURE'),
            page_count=book_json['page_count'],
            # Tambahkan atribut lainnya dari JSON sesuai kebutuhan
        )
        new_book.save()
        authors_list = book_json.get('authors', [])
        for author_name in authors_list:
            # Mencari penulis berdasarkan nama atau membuat penulis baru jika tidak ada
            author, created = Author.objects.get_or_create(name=author_name)
            new_book.authors.add(author)
        images = book_json.get('images',[])
        for img_url in images:
            image = ImageUrl.objects.create(url=img_url)
            new_book.images.add(image)
        categories_name = book_json.get('categories',[])
        for category_name in categories_name:
            category, created = Category.objects.get_or_create(name=category_name)
            new_book.categories.add(category)
        return new_book

    def __str__(self):
        return self.title
    

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    historyId = models.UUIDField()
    text = models.TextField()
    time = models.DateTimeField()

    @classmethod
    def create_history_with_id(cls, user_id, history_id, text, time):
        history = cls(user_id=user_id, historyId=history_id, text=text, time=time)
        history.save()
        return history
    
    @classmethod
    def delete_history_with_user_id(cls, user_id):
        cls.objects.filter(user_id=user_id).delete()
    
    @classmethod
    def delete_history_with_id(cls, user_id, history_id):
        cls.objects.filter(user_id=user_id, historyId=history_id).delete()
    
    @classmethod
    def filter_by_user_id(cls, user_id):
        return cls.objects.filter(user_id=user_id)

    def to_dict(self):
        adjusted_time = self.time + timedelta(hours=7)
        return {
            'user_id': self.user_id,
            'history_id': str(self.historyId),
            'text': self.text,
            'time': adjusted_time.strftime("%Y-%m-%d %H:%M:%S") if self.time else None
            # Tambahkan attribut lainnya jika diperlukan
        }
    
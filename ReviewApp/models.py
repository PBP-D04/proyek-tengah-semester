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


class ReviewV2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    photo = models.TextField()
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)
    
    @classmethod
    def create_with_id(cls, user_id, book_id, content, rating, photo, **kwargs):
        review = cls(
            user_id=user_id,
            book_id=book_id,
            content=content,
            rating=rating,
            photo=photo,
            **kwargs
        )
        review.save()
        return review

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.auth_user.to_dict(),
            'book_id': self.book.id,
            'content': self.content,
            'rating': self.rating,
            'photo_url': self.photo if self.photo else None,
            'date_added': self.date_added.strftime('%Y-%m-%d') if self.date_added else None
            # Tambahkan informasi lain dari model Review yang ingin Anda sertakan di sini
        }
    
####################################################################################################

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_book')
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    photo = models.ImageField(upload_to='review_photos/', blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.auth_user.to_dict(),
            'book_id': self.book.id,
            'content': self.content,
            'rating': self.rating,
            'photo_url': self.photo.url if self.photo else None,
            'date_added': self.date_added.strftime('%Y-%m-%d') if self.date_added else None
            # Tambahkan informasi lain dari model Review yang ingin Anda sertakan di sini
        }
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from Homepage.models import Book
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
import json

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return obj.url if obj else None
        return super().default(obj)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=5,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    photo = models.ImageField(upload_to='review_photos/', blank=True, null=True)
    date_added = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.id)
    
    # Optional: Method to serialize the instance
    def to_json(self):
        return json.dumps({
            'user': self.user.username,
            'book': self.book.title,
            'content': self.content,
            'rating': self.rating,
            'photo': self.photo.url if self.photo else None,
            'date_added': self.date_added
        }, cls=CustomJSONEncoder)


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from Homepage.models import Book

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
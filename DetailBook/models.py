from datetime import timedelta
from django.db import models
from Homepage.models import Book
from django.contrib.auth.models import User
from Bookphoria.models import UserProfile
import pytz
 
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content[:20]

class CommentV2 (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_book')
    content= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_with_id(cls, user_id, book_id, content, **kwargs):
        comment = cls(user_id=user_id, book_id=book_id, content=content, **kwargs)
        comment.save()
        return comment
    
    def to_dict(self):
        adjusted_time = self.created_at + timedelta(hours=7)
        return {
        
            'username': self.user.username,
            'profile_picture': self.user.auth_user.profile_picture,
            'user_id':self.user.pk,
            'book': self.book.pk,
            'content': self.content,
            'created_at': adjusted_time.strftime('%Y-%m-%d %H:%M:%S')# Formatting date as string
        }

    
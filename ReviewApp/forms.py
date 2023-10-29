from django.forms import ModelForm
from ReviewApp.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content', 'photo', 'book']

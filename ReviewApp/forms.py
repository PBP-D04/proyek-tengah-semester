from django.forms import ModelForm
from ReviewApp.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'review', 'image']

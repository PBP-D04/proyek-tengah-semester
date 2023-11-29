from django.urls import path
from .views import home, coba_coba_review,create_review, get_review_json, get_review_flutter,show_review, add_review_flutter

app_name = 'ReviewApp'

urlpatterns = [
    path('coba-coba-review/', coba_coba_review ),
    path('get-review/', get_review_json, name='get_review_json'),
    path('create-review/', create_review, name='create_review'),
    path('show-review/', show_review, name='show_review'),
    path('add-review-flutter/', add_review_flutter),
    path('get-review-flutter/', get_review_flutter)
]
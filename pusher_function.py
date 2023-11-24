import pusher
from Homepage.models import Book
from django.http import JsonResponse
import json

pusher_client = pusher.Pusher(
  app_id='1713048',
  key='7b3be760fa27ea1935c8',
  secret='5da7fb2217c06dabe93a',
  cluster='ap1',
  ssl=True
)

async def dummy_check_is_ok(): 
    pusher_client.trigger('bookphoria', 'dummy', {'message': 'ada manusia terkuat'}) # nama channel, nama event, message

def update_book_like(user_id, book_id, is_liked):
    status_json = json.dumps({'user_id':user_id, 'book_id':book_id, 'is_liked':is_liked})
    pusher_client.trigger('bookphoria', 'like-book', {'message':status_json}) # nama channel, nama event, message
    

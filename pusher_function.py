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

def create_new_book(book_data):
    book_json =json.dumps(book_data)
    pusher_client.trigger('bookphoria', 'new-book',{'message':book_json})  
def realtime_update_comment(comment):
    pusher_client.trigger('bookphoria', 'new-comment', {'message':comment})
def realtime_update_review(review):
    pusher_client.trigger('bookphoria', 'new-review', {'message':review})
def realtime_delete_review(idToDelete):
    pusher_client.trigger('bookphoria', 'delete-review', {'message': idToDelete})

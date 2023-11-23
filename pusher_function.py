import pusher

pusher_client = pusher.Pusher(
  app_id='1713048',
  key='7b3be760fa27ea1935c8',
  secret='5da7fb2217c06dabe93a',
  cluster='ap1',
  ssl=True
)

async def dummy_check_is_ok(): 
    pusher_client.trigger('bookphoria', 'dummy', {'message': 'ada manusia terkuat'}) # nama channel, nama event, message



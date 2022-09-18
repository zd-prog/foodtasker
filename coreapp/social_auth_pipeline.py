import profile
from urllib import request
from coreapp.models import Customer, Driver

def create_user_by_type(backend, user, response, *args, **kwargs):
  request = backend.strategy.request_data()

  if backend.name == 'facebook':
    avatar = 'https://graph.facebook.com/%s/picture?type=large' % response['id']

    if request['user_type'] == "driver":
      Driver.objects.get_or_create(user_id = user.id, avatar = avatar)
    elif request['user_type'] == "customer":
      Customer.objects.get_or_create(user_id = user.id, avatar = avatar)
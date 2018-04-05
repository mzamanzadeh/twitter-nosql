from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from twitter.utils import *
import json


@csrf_exempt
def register(request):
   body_unicode = request.body.decode('utf-8')
   data = json.loads(body_unicode)

   r = connectToRedis()

   userKey = 'users:'+data['username']

   r.hset(userKey, 'username', data['username'])
   r.hset(userKey, 'fullname', data['fullname'])
   r.hset(userKey, 'email', data['email'])
   r.hset(userKey, 'password', data['password'])

   # request.session['username'] = str(username)

   r.lpush('userSearch',data['username'])
   r.lpush('nameSearch',data['fullname'])

   return json_response({'status': True})

@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    r = connectToRedis()
    if ( r.exists("users:"+data['username']) == 1 ):
     if r.hget(data['username'],'password') == data['password']:
        request.session['username'] = data['username']
        return json_response({'status': True})
     else:
        return json_response({'status': False},401)

    else:
      return json_response({'status': False},401)


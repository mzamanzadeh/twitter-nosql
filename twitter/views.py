from django.shortcuts import render
# Create your views here.
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from twitter.auth.login_check import login_check
from twitter.utils import *
import json

@login_check
def index(request):
    return json_response(request.userinfo.get("email"))

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
     if r.hget("users:"+data['username'],'password').decode("utf-8")  == data['password']:
        token = generateToken(data['username'])
        return json_response({'token': token})
     else:
        return json_response({'status': False},401)

    else:
      return json_response({'status': False},401)

def generateToken(username):
    r = connectToRedis()
    newToken = get_random_string(32)
    key = "tokens:" + newToken
    r.hset(key,"username", username)
    return newToken

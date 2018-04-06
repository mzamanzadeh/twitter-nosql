import time
from django.shortcuts import render
# Create your views here.
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from twitter.auth.login_check import login_check
from twitter.utils import *
import json
from datetime import datetime

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


   r.lpush('search:fullname',data['fullname'].lower())
   r.lpush('search:username',data['username'].lower())

   return json_response({'status': True})

@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    r = connectToRedis()
    if ( r.exists("users:"+data['username']) == 1 ):
     if r.hget("users:"+data['username'],'password') == data['password']:
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

@login_check
def userInfo(request):
    ret = {
        'fullname': request.userinfo.get("fullname"),
        'username': request.userinfo.get("username"),
        'avatar': "/hajiax",
        'email': request.userinfo.get("email"),
    }
    return json_response(ret)

@csrf_exempt
@login_check
def newTweet(request):
    import re
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    now = time.time()

    tweetKey = "tweets:" + request.username + ":"+ str(int(now))

    r.hset(tweetKey, 'text', data['tweet'])
    r.hset(tweetKey, 'by', request.username)
    r.hset(tweetKey, 'likes', 0)
    r.hset(tweetKey, 'retweeted', 0)
    r.hset(tweetKey, 'isRetweet', 0)
    r.hset(tweetKey, 'createdAt', now)

    r.rpush("tweets:"+request.username, tweetKey)

    # push into follower's timeline (sorted by time)
    for followerIndex in range(0, r.llen("followers:"+request.username)):
        r.zadd( "timelines:" + r.lindex("followers:"+request.username, followerIndex), now, tweetKey)

    #find hashtags
    hashtags = re.findall(r"#(\w+)", data['tweet'])

    for hashtag in hashtags:
        r.rpush("hashtags:"+hashtag, tweetKey)
        r.zincrby("hashtags::trends", hashtag, amount= 1)

    ret = {
        'success': True,
    }
    return json_response(ret)

@csrf_exempt
@login_check
def listTweet(request):
    import re
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    now = time.time()

    tweetKey = "tweets:" + request.username + ":"+ str(int(now))

    r.hset(tweetKey, 'text', data['tweet'])
    r.hset(tweetKey, 'likes', 0)
    r.hset(tweetKey, 'retweeted', 0)
    r.hset(tweetKey, 'retweetFrom', None)
    r.hset(tweetKey, 'createdAt', now)

    r.rpush("tweets:"+request.username, tweetKey)

    # push into follower's timeline (sorted by time)
    for followerIndex in range(0, r.llen("followers:"+request.username)):
        r.zadd( "timelines:" + r.lindex("followers:"+request.username, followerIndex), now, tweetKey)

    #find hashtags
    hashtags = re.findall(r"#(\w+)", data['tweet'])

    for hashtag in hashtags:
        r.rpush("hashtags:"+hashtag, tweetKey)
        r.zincrby("hashtags:trends", hashtag, amount= 1)

    ret = {
        'success': True,
    }
    return json_response(ret)


@login_check
def myTweets(request):
    r = connectToRedis()
    tweets = []
    for tweetKey in r.lrange("tweets:" + request.username,0,-1):
        tweets.append(fetchTweet(tweetKey))

    return json_response({'tweets':tweets})


@login_check
def timeline(request):

    r = connectToRedis()

    result = []

    for tweetKey in r.zrange("timelines:" + request.username,0,-1,desc=True):
        result.append(fetchTweet(tweetKey))

    return json_response(result)

@login_check
def trends(request):

    r = connectToRedis()

    result = r.zrange("hashtags::trends", 0, 10, desc=True, withscores=True)

    return json_response(result)

@csrf_exempt
@login_check
def searchUsers(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    result = []
    word = data['query'].lower()
    for x in range(0, r.llen("search:fullname")):
        if (word in r.lindex("search:fullname", x) or word in r.lindex("search:username", x)):
            result.append({"username": r.lindex("search:username", x), "fullname": r.lindex("search:fullname", x)})

    return json_response(result)

@csrf_exempt
def searchHashtags(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    result = []
    word = data['query']

    for tweetKey in r.lrange("hashtags:"+word,0,-1):
        result.append(fetchTweet(tweetKey))

    return json_response(result)


@csrf_exempt
@login_check
def follow(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    r.sadd("followers:"+data['username'],request.username)
    r.sadd("followings:"+request.username,data['username'])

    for tweetKey in r.lrange("tweets:"+data['username'],0,-1):
        t = fetchTweet(tweetKey)
        r.zadd("timelines:"+request.username, float(t.get('createdAt')), tweetKey)

    return json_response({'success': True})

@csrf_exempt
@login_check
def unfollow(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    r.srem("followers:"+data['username'],request.username)
    r.srem("followings:" + request.username, data['username'])

    for tweetKey in r.lrange("tweets:" + data['username'],0,-1):
        r.zrem("timelines:"+request.username, tweetKey)

    return json_response({'success': True})

@login_check
def followers(request):
    r = connectToRedis()
    results = r.smembers("followers:" + request.username)
    return json_response(results)

@login_check
def followings(request):
    r = connectToRedis()
    results = r.smembers("followings:" + request.username)
    return json_response(results)

@csrf_exempt
@login_check
def retweet(request):
    import re
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    r = connectToRedis()

    tweet = fetchTweet(data['key'])
    now = time.time()
    tweetKey = "tweets:" + request.username + ":" + str(int(now))

    r.hset(tweetKey, 'text', tweet['text'])
    r.hset(tweetKey, 'by', request.username)
    r.hset(tweetKey, 'likes', 0)
    r.hset(tweetKey, 'retweeted', int(tweet['retweeted'])+1)
    r.hset(tweetKey, 'retweetedFrom', tweet['by'])
    r.hset(tweetKey, 'createdAt', now)

    r.rpush("tweets:" + request.username, tweetKey)

    # push into follower's timeline (sorted by time)
    for followerIndex in range(0, r.llen("followers:" + request.username)):
        r.zadd("timelines:" + r.lindex("followers:" + request.username, followerIndex), now, tweetKey)

    # find hashtags
    hashtags = re.findall(r"#(\w+)", data['tweet'])

    for hashtag in hashtags:
        r.rpush("hashtags:" + hashtag, tweetKey)
        r.zincrby("hashtags::trends", hashtag, amount=1)

    return json_response({'success': True})

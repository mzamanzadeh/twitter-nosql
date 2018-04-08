from django.http.response import HttpResponse
from json import dumps
import redis
def json_response(data={}, status=200):
    return HttpResponse(dumps(data),status=status, content_type='application/json')

def connectToRedis():
    return redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True , charset="utf-8")

def fetchTweet(tweetKey):
    return fetch(tweetKey, ['createdAt', 'text', 'by', 'retweeted', 'retweetedFrom', 'likes'])

def fetch(tweetKey ,keys):
    r = connectToRedis()
    tweet = r.hgetall(tweetKey)
    x = {'key': tweetKey}
    for key in keys:
        x[key] = tweet.get(key)
    return x
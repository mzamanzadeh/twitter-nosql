import csv
import re
from twitter.views import *


def users(request):
    with open(request.GET.get("file"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            res.body = bytes("{\"username\": \""+row[0]+"\"  ,\"password\": \""+row[1]+"\",\"email\": \""+row[0]+"@gmail.com\",\"fullname\": \""+row[0]+"\"}",'utf-8')
            register(res)

def tweets(request,flag=False):
    with open(request.GET.get("file"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        r = connectToRedis()

        now = time.time()

        for row in reader:

            now = now - 300.0
            tweetKey = "tweets:" + row[0] + ":" + str(int(now))

            r.hset(tweetKey, 'text', row[1])
            r.hset(tweetKey, 'by', row[0])
            r.hset(tweetKey, 'likes', row[2])
            r.hset(tweetKey, 'retweeted', 0)

            if flag==True:
                r.hset(tweetKey, 'retweetedFrom', "CSV")

            r.hset(tweetKey, 'createdAt', now)

            r.lpush("tweets:" + row[0], tweetKey)

            # push into follower's timeline (sorted by time)
            for follower in r.smembers("followers:" + row[0]):
                r.zadd("timelines:" + follower, now, tweetKey)
            r.zadd("timelines:" + row[0], now, tweetKey)

            # find hashtags
            hashtags = re.findall(r"#(\w+)", row[1])

            for hashtag in hashtags:
                r.rpush("hashtags:" + hashtag, tweetKey)
                r.zincrby("hashtags::trends", hashtag, amount=1)

def follow(request):
    with open(request.GET.get("file"), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        r = connectToRedis()

        now = time.time()

        for row in reader:
            now = now-300
            r.sadd("followers:" + row[1], row[0])
            r.sadd("followings:" + row[0], row[1])

            r.lpush("logs:" + row[0],
                    row[0]+" followed " + row[1] + " at " + datetime.now().strftime("%d, %b %Y %H:%m"))
            r.lpush("logs:" + row[1],
                    row[0] + " has followed "+row[1]+" at " + datetime.now().strftime("%d, %b %Y %H:%m"))

            for tweetKey in r.lrange("tweets:" + row[1], 0, -1):
                t = fetchTweet(tweetKey)
                r.zadd("timelines:" + row[0], float(t.get('createdAt')), tweetKey)


def retweets(request):
    tweets(request,True)

class res:
    body = None
    username = None


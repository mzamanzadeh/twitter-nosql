from django.http.response import HttpResponse
from json import dumps
import redis
def json_response(data={}, status=200):
    return HttpResponse(dumps(data),status=status, content_type='application/json')

def connectToRedis():
    return redis.StrictRedis(host='localhost', port=6379, db=0)
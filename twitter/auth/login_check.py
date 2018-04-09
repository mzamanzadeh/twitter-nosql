from django.core.exceptions import PermissionDenied
from twitter.utils import *

def login_check(function):
    def wrap(request, *args, **kwargs):
        r = connectToRedis()
        if r.exists("tokens:"+request.META.get('HTTP_AUTHORIZATION',"")):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
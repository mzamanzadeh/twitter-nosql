from twitter.utils import *
def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):

        r = connectToRedis()

        token = request.META.get('HTTP_AUTHORIZATION')

        if r.exists("tokens:"+token):
            username =  r.hget("tokens:"+token,"username").decode("utf-8")
            request.userinfo =  r.hgetall("users:"+username)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
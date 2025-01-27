import http
import json

from django.http import HttpResponse

from users.models import Token


def token_exists(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        try:
            token = Token.objects.get(key=json_post['token'])
            request.user = token.user
            request.json_post = json_post
        except Token.DoesNotExist:
            return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper

import http
import json

from django.http import HttpResponse, JsonResponse

from users.models import Token


def token_exists(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        try:
            token = Token.objects.get(key=json_post['token'])
            request.user = token.user
        except Token.DoesNotExist:
            return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def required_method(method_type):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method_type:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def load_json_body(func):
    def wrapper(request, *args, **kwargs):
        try:
            json_body = json.loads(request.body)
            request.json_body = json_body
        except:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def required_fields(*fields, model):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            json_body = json.loads(request.body)
            try:
                for field in fields:
                    field = model.objects.get(key=json_body[field])
            except:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

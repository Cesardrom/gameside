import http
import json

from django.http import JsonResponse

from users.models import Token


def verify_token(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        try:
            token = Token.objects.get(key=json_post['token'])
            request.user = token.user
        except Token.DoesNotExist:
            return JsonResponse(
                {'error': 'Unknown authentication token'}, status=http.HTTPStatus.UNAUTHORIZED
            )
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
            # Verifica si el cuerpo de la solicitud está vacío
            if not request.body:
                return JsonResponse({'error': 'Missing request body'}, status=400)

            # Intenta cargar el cuerpo como JSON
            request.json_body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        except Exception as e:
            # Esto capturará otros posibles errores
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

        return func(request, *args, **kwargs)

    return wrapper


def required_fields(*fields, model):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            json_body = json.loads(request.body)
            for field in fields:
                if field not in json_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

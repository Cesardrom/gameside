from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import load_json_body, required_fields, required_method

from .models import Token


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('username', 'password', model=Token)
def auth(request):
    username = request.json_body['username']
    password = request.json_body['password']

    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'token': user.token.key}, status=200)

from django.http import JsonResponse

from .models import Token


def auth(request):
    token = Token.objects.get(key=request.json_body['token'])
    return JsonResponse({'token': token})

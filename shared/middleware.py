from django.http import JsonResponse

from .error import ApiError


class ApiErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except ApiError:
            return JsonResponse({'error': ApiError.message}, ApiError.status)

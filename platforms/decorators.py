from django.http import JsonResponse

from .models import Platform


def verify_platform(func):
    def wrapper(request, platform_slug, *args, **kwargs):
        try:
            platform = Platform.objects.get(slug=platform_slug)
            request.platform = platform
        except Platform.DoesNotExist:
            return JsonResponse({'error': 'Platform not found'}, status=404)
        return func(request, platform_slug, *args, **kwargs)

    return wrapper

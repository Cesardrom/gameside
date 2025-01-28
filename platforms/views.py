from django.http import JsonResponse
from django.shortcuts import get_list_or_404

from shared.decorators import required_method

from .models import Platform
from .serializers import PlatformSerializer


# Create your views here.
@required_method('GET')
def platform_list(request):
    platforms = get_list_or_404(Platform)
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@required_method('GET')
def platform_detail(request, platform_slug):
    try:
        platform = Platform.objects.get(slug=platform_slug)
    except Platform.DoesNotExist:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

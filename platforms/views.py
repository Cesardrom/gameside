from django.http import JsonResponse

from shared.decorators import required_method

from .models import Platform
from .serializers import PlatformSerializer


# Create your views here.
@required_method('GET')
def platform_list(request):
    platforms = Platform.objects.all()
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

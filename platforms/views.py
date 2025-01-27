from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Platform
from .serializers import PlatformSerializer


# Create your views here.
def platform_list(request):
    platforms = get_list_or_404(Platform)
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


def platform_detail(request, platform_slug):
    platform = get_object_or_404(Platform, slug=platform_slug)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

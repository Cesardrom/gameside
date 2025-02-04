from shared.decorators import required_method

from .decorators import verify_platform
from .models import Platform
from .serializers import PlatformSerializer


@required_method('GET')
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@required_method('GET')
@verify_platform
def platform_detail(request, platform_slug):
    serializer = PlatformSerializer(request.platform, request=request)
    return serializer.json_response()

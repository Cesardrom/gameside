from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.serializers import serialize
from .models import Platform
from django.http import JsonResponse


# Create your views here.
def platform_list(request):
    platforms = get_list_or_404(Platform)
    platform_json=serialize('json',platforms)
    return JsonResponse(platform_json,safe=False)


def platform_detail(request, platform_slug):
    platform = get_object_or_404(Platform, slug=platform_slug)

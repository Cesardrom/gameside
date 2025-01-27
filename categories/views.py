from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import Category
from .serializers import CategorySerializer


# Create your views here.
@csrf_exempt
@require_GET
def category_list(request):
    categories = get_list_or_404(Category)
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


@csrf_exempt
@require_GET
def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

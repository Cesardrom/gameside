from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Category
from .serializers import CategorySerializer


# Create your views here.
def category_list(request):
    categories = get_list_or_404(Category)
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

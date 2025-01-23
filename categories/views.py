from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Category


# Create your views here.
def category_list(request):
    categories = get_list_or_404(Category)
    categories_json=serialize('json',categories)
    return JsonResponse(categories_json,safe=False)


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    pass

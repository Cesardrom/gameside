from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Category


# Create your views here.
def category_list(request):
    categories = get_list_or_404(Category)
    pass


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    pass

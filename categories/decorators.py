from django.http import JsonResponse

from .models import Category


def verify_category(func):
    def wrapper(request, category_slug, *args, **kwargs):
        try:
            category = Category.objects.get(slug=category_slug)
            request.category = category
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return func(request, category_slug, *args, **kwargs)

    return wrapper

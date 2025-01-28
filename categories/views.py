from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import Category
from .serializers import CategorySerializer


# Create your views here.
@csrf_exempt
@require_GET
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


@csrf_exempt
@require_GET
def category_detail(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

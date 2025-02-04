from django.views.decorators.csrf import csrf_exempt

from shared.decorators import required_method

from .decorators import verify_category
from .models import Category
from .serializers import CategorySerializer


# Create your views here.
@csrf_exempt
@required_method('GET')
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_category
def category_detail(request, category_slug):
    serializer = CategorySerializer(request.category, request=request)
    return serializer.json_response()

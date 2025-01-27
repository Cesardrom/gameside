from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from shared.decorators import token_exists

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@require_POST
@token_exists
def add_order(request):
    pass


@csrf_exempt
@require_POST
@token_exists
def order_detail(request, order_pk: int):
    order = get_object_or_404(Order, pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@require_POST
@token_exists
def confirm_order(request, order_pk: int):
    pass


@csrf_exempt
@require_POST
@token_exists
def cancel_order(request, order_pk: int):
    pass


@csrf_exempt
@require_POST
@token_exists
def pay_order(request, order_pk: int):
    pass

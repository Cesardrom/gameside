from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import load_json_body, required_fields, required_method

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields(model=Order)
def add_order(request):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields(model=Order)
def order_detail(request, order_pk: int):
    order = get_object_or_404(Order, pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields(model=Order)
def confirm_order(request, order_pk: int):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields(model=Order)
def cancel_order(request, order_pk: int):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields(model=Order)
def pay_order(request, order_pk: int):
    pass

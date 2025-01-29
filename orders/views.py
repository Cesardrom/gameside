from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from games.serializers import GameSerializer
from shared.decorators import load_json_body, required_fields, required_method, verify_token
from users.models import Token

from .helpers import order_validator
from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def add_order(request):
    token = Token.objects.get(key=request.json_body['token'])
    user = token.user
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def order_detail(request, order_pk: int):
    order = get_object_or_404(Order, pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def order_game_list(request, order_pk: int):
    order = order_validator(order_pk)
    if order:
        if order.user.pk == request.user.pk:
            games = order.games.all()
            serializer = GameSerializer(games, request=request)
            return serializer.json_response()
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def add_game_to_order(request, order_pk: int, game_slug: str):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def confirm_order(request, order_pk: int):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def cancel_order(request, order_pk: int):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
def pay_order(request, order_pk: int):
    pass

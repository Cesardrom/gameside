from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import load_json_body, required_fields, required_method, verify_token

from .decorators import (
    validate_credit_card,
    verify_confirmed,
    verify_game_in_order,
    verify_order,
    verify_status,
    verify_user,
)
from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@required_method('POST')
@verify_token
def add_order(request):
    user = request.user
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk})


@csrf_exempt
@required_method('GET')
@verify_token
@verify_order
@verify_user
def order_detail(request, order_pk: int):
    serializer = OrderSerializer(request.order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_token
@verify_order
@verify_user
def order_game_list(request, order_pk: int):
    games = request.order.games.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('game-slug', model=Game)
@verify_token
@verify_order
@verify_game_in_order
@verify_user
def add_game_to_order(request, order_pk: int):
    game = request.game
    request.order.add(game)
    request.order.decrease_stock()
    return JsonResponse({'num-games-in-order': request.order.games.count()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('status', model=Order)
@verify_token
@verify_order
@verify_user
@verify_status('confirmed')
def change_order_status(request, order):
    VALID_STATUS = [2, -1]
    status = request.json_body['status']
    if status not in VALID_STATUS:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    if status == -1:
        request.order.increase_stock()
    request.order.update_status(status)
    return JsonResponse({'status': request.order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@verify_user
@verify_confirmed
@validate_credit_card
def pay_order(request, order_pk: int):
    request.order.update_status(3)
    return JsonResponse({'status': request.order.get_status_display(), 'keys': request.order.key})

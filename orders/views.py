from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.serializers import GameSerializer
from shared.decorators import load_json_body, required_fields, required_method, verify_token

from .decorators import (
    verify_confirmed,
    verify_game_in_order,
    verify_order,
    verify_status,
    verify_user,
)
from .models import Order
from .serializers import OrderSerializer
from .validators import validate_card_data


@csrf_exempt
@required_method('GET')
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
@required_method('GET')
@verify_token
@verify_order
@verify_game_in_order
@verify_user
def add_game_to_order(request, order_pk: int, game_slug: str):
    request.order.add(game_slug)
    return JsonResponse({'num-games-in-order': request.order.games.count()})


@csrf_exempt
@required_method('GET')
@verify_token
@verify_order
@verify_user
@verify_status('confirmed')
def confirm_order(request, order):
    request.order.update_status(2)
    return JsonResponse({'status': request.order.get_status_display()})


@csrf_exempt
@required_method('GET')
@verify_token
@verify_order
@verify_user
@verify_status('cancelled')
def cancel_order(request, order_pk: int):
    request.order.update_status(-1)
    request.order.increase_stock()
    return JsonResponse({'status': request.order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@verify_user
@verify_confirmed
def pay_order(request, order_pk: int):
    card_number = request.json_body['card-number']
    exp_date = request.json_body['exp-date']
    cvc = request.json_body['cvc']

    validation_error = validate_card_data(card_number, exp_date, cvc)
    if validation_error:
        return JsonResponse(validation_error, status=400)
    request.order.update_status(3)
    game_keys = [game.key for game in request.order.games.all()]
    return JsonResponse({'status': request.order.get_status_display(), 'keys': game_keys})

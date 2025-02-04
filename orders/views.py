from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import load_json_body, required_fields, required_method, verify_token
from users.models import Token

from .decorators import verify_confirmed, verify_game, verify_order, verify_status, verify_user
from .models import Order
from .serializers import OrderSerializer
from .validators import validate_card_data


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
@verify_order
@verify_user
def order_detail(request, order_pk: int):
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
@verify_order
@verify_user
def order_game_list(request, order_pk: int):
    order = Order.objects.get(pk=order_pk)
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
@verify_order
@verify_game
@verify_user
def add_game_to_order(request, order_pk: int, game_slug: str):
    order = Order.objects.get(pk=order_pk)
    game = Game.objects.get(slug=game_slug)
    order.games.add(game)
    order.save()
    print(order.games.count())
    return JsonResponse({'num-games-in-order': order.games.count()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
@verify_order
@verify_user
@verify_status('confirmed')
def confirm_order(request, order):
    token = Token.objects.get(key=request.json_body['token'])
    user = token.user
    order = Order.objects.get(user=user, status=1)
    order.update_status(2)
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
@verify_order
@verify_user
@verify_status('cancelled')
def cancel_order(request, order_pk: int):
    token = Token.objects.get(key=request.json_body['token'])
    user = token.user
    order = Order.objects.get(user=user)
    order.update_status(-1)
    order.increase_stock()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', 'card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@verify_user
@verify_confirmed
def pay_order(request, order_pk: int):
    card_number = request.json_body['card-number']
    exp_date = request.json_body['exp-date']
    cvc = request.json_body['cvc']
    print(card_number, exp_date, cvc)

    validation_error = validate_card_data(card_number, exp_date, cvc)
    if validation_error:
        return JsonResponse(validation_error, status=400)

    order = Order.objects.get(pk=order_pk)
    order.update_status(3)
    game_keys = [game.key for game in order.games.all()]
    return JsonResponse({'status': order.get_status_display(), 'keys': game_keys})

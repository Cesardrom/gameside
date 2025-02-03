from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.serializers import GameSerializer
from shared.decorators import load_json_body, required_fields, required_method, verify_token
from users.models import Token

from .decorators import verify_order, verify_status, verify_user
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
@verify_user
def add_game_to_order(request, order_pk: int, game_slug: str):
    pass


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
@verify_user
@verify_order
@verify_status('confirmed')
def confirm_order(request, order):
    token = Token.objects.get(key=request.json_body['token'])
    user = token.user
    order = Order.objects.get(user=user, status=1)
    order.status = 2
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', model=Order)
@verify_token
@verify_user
@verify_order
@verify_status('cancelled')
def cancel_order(request, order_pk: int):
    token = Token.objects.get(key=request.json_body['token'])
    user = token.user
    order = Order.objects.get(user=user)
    order.status = -1
    order.increase_stock()
    order.save()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', 'card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
def pay_order(request, order_pk: int):
    card_number = request.POST.get('card_number')
    exp_date = request.POST.get('exp_date')
    cvc = request.POST.get('cvc')

    validation_error = validate_card_data(card_number, exp_date, cvc)
    if validation_error:
        return JsonResponse(validation_error, status=400)

    order = request.order
    if order.status != 'initiated':
        return JsonResponse({'error': 'Orders can only be paid when initiated'}, status=400)

    game_keys = [game.key for game in order.games.all()]
    return JsonResponse({'status': order.get_status_display(), 'keys': game_keys})

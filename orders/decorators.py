from django.http import JsonResponse

from games.models import Game

from .models import Order


def verify_user(func):
    def wrapper(request, order_pk, *args, **kwargs):
        order = Order.objects.get(pk=order_pk)

        if order.user != request.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(request, order_pk, *args, **kwargs)

    return wrapper


def verify_order(func):
    def wrapper(request, order_pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_pk)
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(request, order_pk, *args, **kwargs)

    return wrapper


def verify_status(status):
    def function(func):
        def wrapper(request, order_pk, *args, **kwargs):
            order = Order.objects.get(pk=order_pk)
            if order.status != 1:
                return JsonResponse(
                    {'error': f'Orders can only be {status.lower()} when initiated'}, status=400
                )
            return func(request, order_pk, *args, **kwargs)

        return wrapper

    return function


def verify_confirmed(func):
    def wrapper(request, order_pk, *args, **kwargs):
        order = Order.objects.get(pk=order_pk)
        if order.status != 2:
            return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
        return func(request, order_pk, *args, **kwargs)

    return wrapper


def verify_game_in_order(func):
    def wrapper(request, order_pk, game_slug, *args, **kwargs):
        try:
            game = Game.objects.get(slug=game_slug)
            request.game = game
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, order_pk, game_slug, *args, **kwargs)

    return wrapper

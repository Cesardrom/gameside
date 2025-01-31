from django.http import JsonResponse

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

from .models import Order


def order_validator(order_pk):
    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return False
    return order

from django.shortcuts import get_object_or_404

from .models import Order


def add_order(request):
    pass


def order_detail(request, order_pk: int):
    order = get_object_or_404(Order, pk=order_pk)


def confirm_order(request, order_pk: int):
    pass


def cancel_order(request, order_pk: int):
    pass


def pay_order(request, order_pk: int):
    pass

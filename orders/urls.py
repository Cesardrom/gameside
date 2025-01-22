from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('<int:pk>/confirm/', views.confirm_order, name='order-confirm'),
    path('<int:pk>/cancel/', views.cancel_order, name='order-cancel'),
    path('<int:pk>/pay/', views.pay_order, name='order-pay'),
]

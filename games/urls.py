from django.urls import path, register_converter

from . import views
from .converters import GameConverter

register_converter(GameConverter, 'game')
app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('filter', views.game_list, name='game-list'),
    path('<str:game_slug>/', views.game_detail, name='game-detail'),
    path('<str:game_slug>/reviews/', views.review_list, name='review-list'),
    path('reviews/<int:review_pk>/', views.review_detail, name='review-detail'),
    path('<str:game_slug>/reviews/add/', views.add_review, name='add-review'),
]

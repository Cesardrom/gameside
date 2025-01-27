from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


# Create your views here.
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


def game_detail(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


def review_list(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = get_list_or_404(Review, game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


def review_detail(request, review_pk: int):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


def add_review(request, game_slug: str):
    pass

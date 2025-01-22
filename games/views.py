from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Game, Review


# Create your views here.
def game_list(request):
    games = get_list_or_404(Game)


def game_detail(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)


def review_list(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = get_list_or_404(Review, game=game)


def review_detail(request, review_pk: int):
    review = get_object_or_404(Review, pk=review_pk)


def add_review(request, game_slug: str):
    pass

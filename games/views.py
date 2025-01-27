from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Game, Review
from .serializers import GameSerializer


# Create your views here.
def game_list(request):
    game = Game.objects.all()
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


def game_detail(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    game_json = serialize('json', game)
    return JsonResponse(game_json, safe=False)


def review_list(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = get_list_or_404(Review, game=game)
    reviews_json = serialize('json', reviews)
    return JsonResponse(reviews_json, safe=False)


def review_detail(request, review_pk: int):
    review = get_object_or_404(Review, pk=review_pk)


def add_review(request, game_slug: str):
    pass

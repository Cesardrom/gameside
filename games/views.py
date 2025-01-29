from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import load_json_body, required_fields, required_method, token_exists

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@csrf_exempt
@required_method('GET')
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
def game_detail(request, game_slug: str):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
def review_list(request, game_slug: str):
    game = get_object_or_404(Game, slug=game_slug)
    reviews = get_list_or_404(Review, game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
def review_detail(request, review_pk: int):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('token', 'rating', 'comment', model=Review)
@token_exists
def add_review(request, game_slug: str):
    game = Game.objects.get(slug=game_slug)
    review = Review.objects.create(
        rating=request.json_body['rating'],
        comment=request.json_body['comment'],
        author=request.user,
        game=game,
    )
    return JsonResponse({'id': review.pk})

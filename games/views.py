from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import load_json_body, required_fields, required_method, verify_token

from .decorators import review_not_found, verify_game
from .helpers import validate_rating
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@csrf_exempt
@required_method('GET')
def game_list(request):
    if len(request.GET) == 2:
        category_slug = request.GET.get('category')
        platform_slug = request.GET.get('platform')
        games = Game.objects.filter(category__slug=category_slug, platforms__slug=platform_slug)
    elif category_slug := request.GET.get('category'):
        games = Game.objects.filter(category__slug=category_slug)
    elif platform_slug := request.GET.get('platform'):
        games = Game.objects.filter(platforms__slug=platform_slug)
    else:
        games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_game
def game_detail(request, game):
    serializer = GameSerializer(request.game, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_game
def review_list(request, game_slug: str):
    reviews = Review.objects.filter(game=request.game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@review_not_found
def review_detail(request, review_pk: int):
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('rating', 'comment', model=Review)
@verify_token
@verify_game
def add_review(request, game_slug: str):
    if rating := validate_rating(request):
        comment = request.json_body['comment']
        review = Review.objects.create(
            rating=rating, author=request.user, comment=comment, game=request.game
        )
        return JsonResponse({'id': review.pk})
    return JsonResponse({'error': 'Rating is out of range'}, status=400)

from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from categories.models import Category
from platforms.models import Platform
from shared.decorators import load_json_body, required_fields, required_method, verify_token

from .helpers import game_validator
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


""" @csrf_exempt
@required_method('GET')
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response() """


@csrf_exempt
@required_method('GET')
def game_list(request):
    if category_slug := request.GET.get('category'):
        category = Category.objects.get(slug=category_slug)
        print(category.pk)
        games = Game.objects.filter(category=category.pk)
        print(games)
    elif platform_slug := request.GET.get('platform'):
        platform = Platform.objects.get(slug=platform_slug)
        games = Game.objects.filter(platforms=platform.pk)
    elif len(request.GET) == 2:
        category_slug = request.GET.get('category')
        platform_slug = request.GET.get('platform')
        category = Category.objects.get(slug=category_slug)
        platform = Platform.objects.get(slug=platform_slug)
        games = Game.objects.filter(category=category.pk, platforms=platform.pk)
    else:
        games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
def game_detail(request, game_slug: str):
    game = game_validator(game_slug)
    if game:
        serializer = GameSerializer(game, request=request)
        return serializer.json_response()
    return JsonResponse({'error': 'Game not found'}, status=404)


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
@verify_token
def add_review(request, game_slug: str):
    game = game_validator(game_slug)
    if game:
        rating = request.json_body['rating']
        comment = request.json_body['comment']
        author = request.user
        game = game
        if 0 < rating <= 5:
            review = Review.objects.create(rating=rating, author=author, comment=comment, game=game)
            return JsonResponse({'id': review.pk})
        else:
            return JsonResponse({'error': 'Rating is out of range'}, status=400)
    return JsonResponse({'error': 'Game not found'}, status=404)

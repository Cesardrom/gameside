from django.http import JsonResponse

from .models import Game, Review


def verify_game(func):
    def wrapper(request, game_slug, *args, **kwargs):
        try:
            game = Game.objects.get(slug=game_slug)
            request.game = game
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, game_slug, *args, **kwargs)

    return wrapper


def review_not_found(func):
    def wrapper(request, review_pk, *args, **kwargs):
        try:
            review = Review.objects.get(pk=review_pk)
            request.review = review
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
        return func(request, review_pk, *args, **kwargs)

    return wrapper

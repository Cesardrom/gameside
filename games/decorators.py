from django.http import JsonResponse

from .models import Game


def verify_game(func):
    def wrapper(request, game_slug, *args, **kwargs):
        try:
            game = Game.objects.get(slug=game_slug)
            request.game = game
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, game_slug, *args, **kwargs)

    return wrapper

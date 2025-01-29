from .models import Game


def game_validator(game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return False
    return game

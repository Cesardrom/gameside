from .models import Game


def game_validator(game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return False
    return game


def validate_rating(request):
    rating = request.json_body['rating']
    if 0 < rating <= 5:
        return rating
    return False

from django.http import JsonResponse

from .models import Game


class GameConverter:
    regex = '[a-z0-9-]+'

    def to_python(self, value):
        try:
            game = Game.objects.get(slug=value)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return game

    def to_url(self, value):
        return value.slug

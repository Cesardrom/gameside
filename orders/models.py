import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1

    status = models.IntegerField(choices=Status, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders'
    )
    games = models.ManyToManyField('games.Game', related_name='game_orders', blank=True)

    def __str__(self):
        return f'{self.user} Status:{self.status}'

    @property
    def price(self):
        total = 0
        for game in self.games.all():
            total += game.price
        return float(total)
    
    def increase_stock(self):
        for game in self.games.all():
            game.stock += 1
            game.save()

    def decrease_stock(self):
        for game in self.games.all():
            game.stock -= 1
            game.save()

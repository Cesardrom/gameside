from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True, null=True, upload_to='cache', default='cache/nocover.png')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField(auto_now=False, auto_now_add=False)
    pegi = models.PositiveSmallIntegerField(choices=Pegi)
    category = models.ForeignKey(
        'categories.Category', related_name='game_categories', on_delete=models.Protect
    )
    platforms = models.ManyToManyField(
        'platforms.Platform', related_name='game_platforms', blank=True
    )

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    game = models.ForeignKey('Game', related_name='game_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews'
    )

    def __str__(self):
        return f'{self.comment}:{self.rating}'

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


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
    cover = models.ImageField(
        blank=True, null=True, upload_to='covers', default='covers/default.jpg'
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField(auto_now=False, auto_now_add=False)
    pegi = models.PositiveSmallIntegerField(choices=Pegi)
    category = models.ForeignKey(
        'categories.Category', related_name='game_categories', on_delete=models.SET_NULL, null=True
    )
    platforms = models.ManyToManyField(
        'platforms.Platform', related_name='game_platforms', blank=True
    )

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey('Game', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews'
    )

    def __str__(self):
        return f'{self.author}:{self.rating}'

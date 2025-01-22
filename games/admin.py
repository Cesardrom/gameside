from django.contrib import admin

from .models import Game, Review


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


admin.site.register(Game, GameAdmin)


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)

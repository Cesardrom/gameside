# Register your models here.

from django.contrib import admin

from .models import Token

# Register your models here.


class TokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Token, TokenAdmin)

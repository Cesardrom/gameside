from django.contrib import admin

from .models import Platform

# Register your models here.


class PlatformAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Platform, PlatformAdmin)

from django.contrib import admin

from .models import Category

# Register your models here.


class CategorieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Category, CategorieAdmin)

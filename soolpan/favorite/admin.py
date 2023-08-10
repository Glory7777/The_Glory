from django.contrib import admin
from .models import Favorite

# Register your models here.


class FavAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'like')


admin.site.register(Favorite, FavAdmin)

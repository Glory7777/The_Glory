from django.contrib import admin
from .models import SpUser

class SpuserAdmin(admin.ModelAdmin):
    list_display=('email',)
    
admin.site.register(SpUser, SpuserAdmin)
from django.contrib import admin
from .models import Tal, Comment
# Register your models here.
class DBAdmin(admin.ModelAdmin):
    list_display=('name','company','mtrl')
    
admin.site.register(Tal, DBAdmin)

admin.site.register(Comment)
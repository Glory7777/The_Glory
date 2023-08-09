from django.contrib import admin
from .models import Tal, Comment
# Register your models here.
class DBAdmin(admin.ModelAdmin):
    list_display=('name','company','mtrl')
    
admin.site.register(Tal, DBAdmin)

class CmAdmin(admin.ModelAdmin):
    list_display=('name','body','created_at','color', 'flavor', 'sweet', 'sour', 'carbon', 'total')

admin.site.register(Comment, CmAdmin)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('db/', include('db.urls')),
    path('ac/', include('autocomplete.urls')),
    path('mv/', include('db_move.urls'))

]
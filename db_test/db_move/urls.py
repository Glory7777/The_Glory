from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search1'),
    path('detail/<int:pk>/', views.detail_view, name='detail'),
]
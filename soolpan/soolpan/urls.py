"""
URL configuration for soolpan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spUser.views import RegisterView, LoginView, logout
from DataBase.views import (index, ProductListAPI, ProductDetailAPI, CommentListAPI, CommentDetailAPI, CommentGroupAPI,comment_update ,comment_delete, TalDetailView)
from favorite.views import FavoriteCreate, FavoriteList
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='Tal_Search'),
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('detail/<int:pk>/', TalDetailView.as_view(), name='detail'),
    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>/', ProductDetailAPI.as_view()),
    path('api/comment/', CommentListAPI.as_view()),
    # path('api/comment/<int:pk>/', CommentDetailAPI.as_view()),
    path('api/comments/', CommentGroupAPI.as_view()),
    path('comment/delete/<int:pk>/', comment_delete, name="comment_delete"),
    path('comment/update/<int:pk>/', comment_update, name="comment_update"),
    path('favorite/create', FavoriteCreate.as_view()),
    path('favorite/', FavoriteList.as_view()),
]

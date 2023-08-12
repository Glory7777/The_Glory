from typing import Any, Dict
from django import http
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import FavoriteForm  # order의 form
from .models import Favorite
from DataBase.models import Tal
from spUser.models import SpUser
from django.utils import timezone
# 데코레이터
from spUser.decorators import login_required, Admin_required
from django.utils.decorators import method_decorator
# Create your views here.


@method_decorator(login_required, name='dispatch')
class FavoriteCreate(FormView):
    form_class = FavoriteForm

    def form_valid(self, form):
        post_id = form.data.get('post')
        like = form.data.get('like')
        user_email = self.request.session.get('user')

        existing_favorite = Favorite.objects.filter(
            post_id=post_id, name__email=user_email).first()

        if existing_favorite:
            
            if existing_favorite.like == 0:
                existing_favorite.like = 1
                existing_favorite.register_date = timezone.now()
                existing_favorite.save()
                
            elif existing_favorite.like == 1:
                existing_favorite.like = 0
                existing_favorite.save()
                
        else:
            # Create a new Favorite object
            tal = Tal.objects.get(pk=post_id)
            user = SpUser.objects.get(email=user_email)
            fav = Favorite(name=user, post=tal, like=like)
            fav.save()

        return HttpResponseRedirect(reverse('detail', args=[post_id]))

    # 유효하지 않을 경우

    def form_invalid(self, form):
        # 헤당 제품 페이지로 리다이렉트
        return redirect('/detail/'+str(form.data.get('post_id')))

    # form에다가 인자를 추가하는 메소드
    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({'request': self.request})
        # 세션을 kw에 포함시킴
        return kw


@method_decorator(login_required, name='dispatch')
class FavoriteList(ListView):
    template_name = "favorite_list.html"
    context_object_name = 'fav_list'

    # model = Order 주문된 제품만 가져오므로 쿼리를 통해서 가져옴
    # bcuser__email : Order모델에서 사용자 이메일이 지금 세션의 사용자와 일치하는 대상들을 필터해서 가져옴
    def get_queryset(self, **kwargs):
        queryset = Favorite.objects.filter(
            name__email=self.request.session.get('user')).order_by('-register_date')  # DB에서 싹 가져와서
        return queryset


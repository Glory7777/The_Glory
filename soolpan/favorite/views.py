from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import FavoriteForm  # order의 form
from .models import Favorite
from DataBase.models import Tal
from spUser.models import SpUser
# 데코레이터
from spUser.decorators import login_required, Admin_required
from django.utils.decorators import method_decorator
# Create your views here.


# @method_decorator(login_required, name='dispatch')
class FavoriteCreate(FormView):
    form_class = FavoriteForm
    success_url = "/"

    def form_valid(self, form):
        tal = Tal.objects.get(pk=form.data.get('post'))  # pk에 있는 상품정보 끌어옴
        fav = Favorite(name=SpUser.objects.get(email=self.request.session.get('user')),
                       post=tal,
                       like=form.data.get('like'))
        fav.save()  # 주문내역 저장

        # 주문건수 만큼 재고 감소
        return super().form_valid(form)

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


# @method_decorator(login_required, name='dispatch')
# class OrderList(ListView):
#     template_name = "order_list.html"
#     context_object_name = 'order_list'

#     # model = Order 주문된 제품만 가져오므로 쿼리를 통해서 가져옴
#     # bcuser__email : Order모델에서 사용자 이메일이 지금 세션의 사용자와 일치하는 대상들을 필터해서 가져옴
#     def get_queryset(self, **kwargs):
#         queryset = Order.objects.filter(
#             shopuser__email=self.request.session.get('user'))  # DB에서 싹 가져와서
#         return queryset

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
from django.core.paginator import Paginator
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
            tal = Tal.objects.get(pk=post_id)
                
                #취소했던 좋아요를 다시 좋아하는 로직
            if existing_favorite.like == 0:
                existing_favorite.like = 1
                existing_favorite.register_date = timezone.now()
                existing_favorite.save()
                tal.like = tal.like + 1 
                tal.save()
                
                #좋아요를 취소할 때 로직
            elif existing_favorite.like == 1:
                existing_favorite.like = 0
                existing_favorite.save()
                tal.like = tal.like - 1
                tal.save()                

        else:
            # 나의 주막에 신규 등록
            tal = Tal.objects.get(pk=post_id)
            user = SpUser.objects.get(email=user_email)
            fav = Favorite(name=user, post=tal, like=like)
            fav.save()
            tal.like = tal.like + 1 
            tal.save()

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
    paginate_by = 8  # 페이지당 아이템 수 설정

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Paginator 객체 생성
        paginator = Paginator(self.object_list, self.paginate_by)
        # URL에서 'page' 매개변수를 사용하여 현재 페이지 번호 가져오기
        page_number = self.request.GET.get('page')

        # 현재 페이지의 Page 객체 가져오기
        page_obj = paginator.get_page(page_number)

        # context에 페이지 객체 추가
        context['page_obj'] = page_obj
        return context
    # model = Order 주문된 제품만 가져오므로 쿼리를 통해서 가져옴
    # bcuser__email : Order모델에서 사용자 이메일이 지금 세션의 사용자와 일치하는 대상들을 필터해서 가져옴
    def get_queryset(self, **kwargs):
        queryset = Favorite.objects.filter(
            name__email=self.request.session.get('user'),
            like=1
        ).order_by('-register_date')
        return queryset


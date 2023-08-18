from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tal, Comment
from .forms import DetailForm, CommentForm, UserInputForm
from favorite.models import Favorite
from favorite.forms import FavoriteForm
from spUser.models import SpUser
import random
from .serializers import ProductSerializer, CommentSerializer
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from django.utils import timezone
from pandas import json_normalize
from urllib.request import Request, urlopen
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Avg
from django.core.paginator import Paginator
from .logic import run_conversation, return_api_url
# Create your views here.
# 홈화면 검색/Autocomplete 기능 구현

# index와 index_v1의 차이 --> 검색 후 클릭해서 이동하냐 or 바로 이동하고 없을 경우 에레메시지
# 교체는 url에서 index 부분 교체해서 사용하면 됨 (다른 것 수정할 필요 없음)



def index(request):
    form = UserInputForm(request.POST)
    response = None
    tal_search = []
    
    #API주소 설정하기
    current_site = get_current_site(request) #현재 페이지 도메인 가져오기(127.0.0.1:8000 변경 대응)
    path = reverse('productListapi') #api기본주소 가져오기
    api_url = f"http://{current_site}{path}" #API주소 확정
    
    if request.method == 'POST':
        if 'user_input' in request.POST:
            form = UserInputForm(request.POST)
            if form.is_valid():
                user_input = form.cleaned_data['user_input']
                return_api_url(api_url) #api주소를 전역변수에 저장하는 메소드
                response = run_conversation(user_input) 
                #api정보를 get하는 get_Liqueur_info에서 저장된 전역변수를 api호출할 때 반드시 사용하게 조치
        
        elif 'search_query' in request.POST:
            search_query = request.POST['search_query']
            if search_query:
                search = Tal.objects.filter(name__icontains=search_query)
                total_objects = search.count()

                if total_objects <= 5:
                    tal_search = search
                else:
                    tal_search = random.sample(list(search), 4)

    tals = Tal.objects.all()
    like = tals.order_by('-like')
    best5 = like[:4]

    top_comments = Comment.objects.values('post_id').annotate(avg_total=Avg('total')).order_by('-avg_total')[:4]
    top_comment_ids = [item['post_id'] for item in top_comments]

    top_comments_queryset = Comment.objects.filter(post_id__in=top_comment_ids)
    tal_objects_for_top_comments = Tal.objects.filter(comments__in=top_comments_queryset).distinct()

    return render(request, 'index.html', {
        'form': form,
        'response': response,
        'tals': tals,
        'tal_search': tal_search,
        'best5': best5,
        'top_comments': top_comments_queryset,
        'tal_objects_for_top_comments': tal_objects_for_top_comments,
    })

# def index(request):
#     tals = Tal.objects.all()
    
#     if request.method == 'POST':
#         search_query = request.POST.get('search_query')
#         if search_query:
#             # Assuming you already have the queryset tal_search
#             search = Tal.objects.filter(name__icontains=search_query)

#             # Get the total number of objects in the queryset
#             total_objects = search.count()

#             # If the total number of objects is less than 10, get all objects
#             if total_objects <= 5:
#                 tal_search = search

#             else:
#                 # Randomly select 10 objects
#                 tal_search = random.sample(list(search), 4)
#         else:
#             tal_search = []
#     else:
#         tal_search = []

#     like = tals.order_by('-like')
#     best5 = like[:4]
    
#     top_comments = Comment.objects.values('post_id').annotate(avg_total=Avg('total')).order_by('-avg_total')[:4]
#     top_comment_ids = [item['post_id'] for item in top_comments]
    
#     top_comments_queryset = Comment.objects.filter(post_id__in=top_comment_ids)
#     tal_objects_for_top_comments = Tal.objects.filter(comments__in=top_comments_queryset).distinct()
#     return render(request, 'index.html', {
#         'tals': tals,
#         'tal_search': tal_search,
#         'best5': best5,
#         'top_comments': top_comments_queryset,
#         'tal_objects_for_top_comments': tal_objects_for_top_comments,
#     })
# def index_v1(request):
#     tals = Tal.objects.all()
#     if request.method == 'POST':
#         form = DetailForm(request.POST)
#         if form.is_valid():
#             search_query = request.POST.get('search_query')
#             if search_query:
#                 try:
#                     search = Tal.objects.get(name__exact=search_query)
#                     return redirect('detail', pk=search.pk)
#                 except:
#                     form.add_error('name', '해당하는 술을 찾을 수 없습니다.')
#     else:
#         form=DetailForm()
#     return render(request, 'index.html', {'tals':tals, 'form':form})


class TalDetailView(DetailView):
    model = Tal
    template_name = 'tal_detail.html'
    context_object_name = 'tal_detail'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tal_result = self.object
        #코멘트 데이터 
        comments = tal_result.comments.all().order_by('-id')
        
        context['comments'] = comments #pagnator 기능 추가일..듯?
        #코멘트 입력하는 폼
        comment_form = CommentForm()       
        context['comment_form'] = comment_form
        #즐겨찾기
        favorite_form = FavoriteForm(request=self.request)
        context['form'] = favorite_form        
        #접속한 사람 이메일
        email = self.request.session.get('user')
        context['email'] = email

        #즐겨찾기 object들 리턴(search.like(좋아요 여부 렌더를 위해)
        try:
            try:
                user_instance = SpUser.objects.get(email=email)
                search = Favorite.objects.get(post=tal_result, name=user_instance)
                context['search'] = search
            except:
                pass
        except Favorite.DoesNotExist:
            context['search'] = None

        #아래의 그래프 리턴한 값 수신하여 렌더할 컨텍스트에 추가
        graph_html = self.graph_view(self.object.pk)
        context['graph_html'] = graph_html
        
        #코멘트용 그래프 
        graph_comments = []
        for comment in comments:
            graph_html_comment = self.graph_view_comment(comment.id)
            graph_comments.append(graph_html_comment)
        # context['comments_and_graphs'] = zip(comments, graph_comments) #zip하면 html깨짐

        #주소 리턴 
        path = self.page_share(self.object.pk)
        context['page_path']=path
        
        # Paginator 객체 생성
        paginator = Paginator(comments, self.paginate_by)  # 3 comments per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments_write'] = page_obj #정상작동
        # 페이지네이터 그래프
        paginator = Paginator(graph_comments, self.paginate_by)  # 3 comments per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments_graph'] = page_obj #정상작동
        

        #전체 컨텍스트 리턴
        return context

    def post(self, request, *args, **kwargs):
        tal_result = self.get_object()
        email = self.request.session.get('user')
        if not email:
            return redirect('/login/')
        try:
            user_instance = SpUser.objects.get(email=email)
        except SpUser.DoesNotExist:
            return redirect('/login/')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = tal_result
            comment.name = user_instance
            comment.save()
            return redirect("detail", pk=tal_result.pk)

        context = self.get_context_data() 
        context['comment_form'] = comment_form 
        return self.render_to_response(context)
    
    def graph_view(self, pk):
        try:        
            df1 = pd.DataFrame() #빈 데이터프레임 만들기
            current_site = get_current_site(self.request) #현재 페이지 도메인 가져오기(127.0.0.1:8000 변경 대응)
            path = reverse('comments_api') #api기본주소 가져오기
            api = f"http://{current_site}{path}?post={pk}" #API주소 

            response = urlopen(api) #response 수신
            json_api = response.read().decode("utf-8") #utf-8로 디코딩
            json_file = json.loads(json_api) #json수신
            json_normalized = json_normalize(json_file) #데이터 프레임으로 변경
            df1 = pd.concat([df1, json_normalized]) #df1에 수신 내용 추가
            df2 = df1[['total', 'color', 'flavor', 'sweet','sour','carbon']] #필요 컬럼만 추출
            df2_mean = df2.mean()  #추출 데이터들의 평균값

            df2_mean.index = df2_mean.index.map(lambda x: '총점' if x == 'total' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '색' if x == 'color' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '당도' if x == 'sweet' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '산미' if x == 'sour' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '향' if x == 'flavor' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '탄산감' if x == 'carbon' else x)

            fig = px.line_polar(df2_mean, r=df2_mean.values, theta=df2_mean.index, line_close=True) #레이더 그래프 그리기
            fig.update_traces(fill='toself')

            # 각 꼭짓점에 텍스트 입력
            for i, value in enumerate(df2_mean.values):
                fig.add_trace(go.Scatterpolar(
                    r=[value + 0.1],  # 텍스트 레이블을 원의 중심에서 약간 떨어트리기 위한 값
                    theta=[df2_mean.index[i]],
                    text=[f'{value:.2f}'],  # 소수점 둘째 자리까지 표시
                    mode='text',
                    textfont=dict(size=8),
                ))
            #레이아웃
            fig.update_layout( 
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                    )),
                showlegend=False
            )
            #그래프를 html로 발신, 기본 사이즈 설정
            graph_html = fig.to_html(full_html=False, default_height=400, default_width=600)
            #데이터 리턴 --> 위의 get context에서 내용 수신
            return graph_html
        except:
            pass

    def graph_view_comment(self, id):
        try:
            df1 = pd.DataFrame() #빈 데이터프레임 만들기
            current_site = get_current_site(self.request) #현재 페이지 도메인 가져오기(127.0.0.1:8000 변경 대응)
            path = reverse('comment_api') #api기본주소 가져오기
            api = f"http://{current_site}{path}{id}" #API주소 
            response = urlopen(api) #response 수신
            json_api = response.read().decode("utf-8") #utf-8로 디코딩
            json_file = json.loads(json_api) #json수신
            json_normalized = json_normalize(json_file) #데이터 프레임으로 변경
            df1 = pd.concat([df1, json_normalized]) #df1에 수신 내용 추가
            df2 = df1[['total', 'color', 'flavor', 'sweet','sour','carbon']] #필요 컬럼만 추출
            df2_mean = df2.mean()
            
            df2_mean.index = df2_mean.index.map(lambda x: '총점' if x == 'total' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '색' if x == 'color' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '당도' if x == 'sweet' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '산미' if x == 'sour' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '향' if x == 'flavor' else x)
            df2_mean.index = df2_mean.index.map(lambda x: '탄산감' if x == 'carbon' else x)

            fig = px.line_polar(df2_mean, r=df2_mean.values, theta=df2_mean.index, line_close=True) #레이더 그래프 그리기
            fig.update_traces(fill='toself')

            # 각 꼭짓점에 텍스트 입력
            for i, value in enumerate(df2_mean.values):
                fig.add_trace(go.Scatterpolar(
                    r=[value + 0.1],  # 텍스트 레이블을 원의 중심에서 약간 떨어트리기 위한 값
                    theta=[df2_mean.index[i]],
                    text=[f'{value:.2f}'],  # 소수점 둘째 자리까지 표시
                    mode='text',
                    textfont=dict(size=8),
                ))
            #레이아웃
            fig.update_layout( 
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                    )),
                showlegend=False
            )
            #그래프를 html로 발신, 기본 사이즈 설정
            graph_html_comment = fig.to_html(full_html=False, default_height=300, default_width=300)
            #데이터 리턴 --> 위의 get context에서 내용 수신
            return graph_html_comment
        except:
            pass
    
    def page_share(self, id):
        current_site = get_current_site(self.request) #현재 페이지 도메인 가져오기(127.0.0.1:8000 변경 대응)
        path = reverse('path_detail') #api기본주소 가져오기
        detail_path = f"http://{current_site}{path}{id}" 
        return detail_path

def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    tal_result = comment.post_id
    email = request.session.get('user')
    if not request.session.get('user'):
        return redirect('/login/')
    if SpUser.objects.get(email=email) == comment.name:
        pass
    else:
        raise Http404("권한이 없습니다.")    

    if request.method == "POST":
        form = CommentForm( request.POST, instance=comment )
        if form.is_valid():
            comment = form.save(commit=False)
            spuser= SpUser.objects.get(email=email)
            comment.name = spuser
            comment.created_at = timezone.now()
            comment.save()
            return redirect('detail', pk=tal_result)
    else:
        form=CommentForm(instance=comment)
    return render(request, 'tal_update.html', {'form':form,'comment':comment})
    

def comment_delete(request, pk):

    user_id = request.session.get('user')
    
    if not request.session.get('user'):
        return redirect('/login/')
    comment = Comment.objects.get(pk=pk)  # 유저 정보 관련된 객체만 집어옴
    tal_result = comment.post_id

    if SpUser.objects.get(email=user_id) == comment.name:
        comment.delete()
    else:
        raise Http404("권한이 없습니다.")
    
    return redirect("detail", pk=tal_result)


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Tal.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Tal.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # list() : ListModelMixin에서 제공
        return self.retrieve(request, *args, **kwargs)


class CommentListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all().order_by('post')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all().order_by('post')

    def get(self, request, *args, **kwargs):
        # list() : ListModelMixin에서 제공
        return self.retrieve(request, *args, **kwargs)


class CommentGroupAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        queryset = Comment.objects.all()
        if post_id is not None:
            queryset = queryset.filter(post=post_id)
        return queryset.order_by('post')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# http://127.0.0.1:8000/api/comments/?post=2 하면 2번만 그룹바이 됨.

# 0809 삭제
# self.request.query_params는 Django REST Framework에서 HTTP 요청(request)의 쿼리 매개변수(query parameters)에 접근하는 방법 중 하나입니다. HTTP 요청은 URL에 추가적인 데이터를 전달하기 위해 쿼리 매개변수를 사용할 수 있습니다. 예를 들어, /your/api/endpoint/?post=post_id와 같은 URL에서 post=post_id가 쿼리 매개변수입니다.

# self.request는 현재 요청(request)에 대한 정보를 가지고 있는 객체입니다. self.request.query_params를 사용하면 해당 요청의 쿼리 매개변수에 접근할 수 있습니다.

# self.request.query_params.get('post', None)는 post라는 키(key)를 가진 쿼리 매개변수의 값을 가져오는 코드입니다. get() 메서드는 딕셔너리(dict)에서 특정 키의 값을 가져오는 메서드로, 첫 번째 인수로 찾고자 하는 키를 전달하고, 두 번째 인수로 해당 키가 존재하지 않을 때 반환할 기본값(default value)을 지정할 수 있습니다.

# 위의 코드에서는 post라는 키의 값을 가져오려고 하고, 만약 해당 키가 존재하지 않는다면 기본값으로 None을 지정하였습니다. 따라서 post라는 키의 값을 가져올 수 있으면 해당 값이 변수 post_id에 저장되고, 키가 존재하지 않으면 post_id는 None이 될 것입니다.


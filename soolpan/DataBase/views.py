from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tal, Comment
from .forms import DetailForm, CommentForm
from spUser.models import SpUser
import random
from .serializers import ProductSerializer, CommentSerializer
from rest_framework import mixins
from rest_framework import generics
from spUser.decorators import login_required, Admin_required
from django.utils.decorators import method_decorator

# Create your views here.
#홈화면 검색/Autocomplete 기능 구현

#index와 index_v1의 차이 --> 검색 후 클릭해서 이동하냐 or 바로 이동하고 없을 경우 에레메시지 
#교체는 url에서 index 부분 교체해서 사용하면 됨 (다른 것 수정할 필요 없음)

def index(request): 
    tals = Tal.objects.all()
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
                        # Assuming you already have the queryset tal_search
            search = Tal.objects.filter(name__icontains=search_query)

            # Get the total number of objects in the queryset
            total_objects = search.count()

            # If the total number of objects is less than 10, get all objects
            if total_objects <= 10:
                tal_search = search
            
            else:
                # Randomly select 10 objects
                tal_search = random.sample(list(search), 10)
        else:
            tal_search = []
    else:
        tal_search = []
    return render(request, 'index.html', {'tals':tals, 'tal_search':tal_search})

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

def tal_detail(request, pk):    
    tal_result =  get_object_or_404(Tal,pk=pk)
     #pk=pk인 술의 정보들을 가져오거나 404
     
     #이 술에 달린 댓글들
    comments = tal_result.comments.all() 
    email = request.session.get('user')
    user_instance = SpUser.objects.get(email=email)
    if request.method == "POST":
        comment_form = CommentForm(request.POST) #댓글입력할 폼 
        if not request.session.get('user'): #로그인세션정보가 없을 경우에 로그인 페이지로 돌려보내기
            return redirect('/login/')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) #커밋을 완료하면 수정삭제가 안됨
            #Commit=false : db안에 즉시 저장하지 말고 객체를 반환하여 수정을 허용
            comment.post = tal_result
            comment.name = user_instance
            comment.save()
            return redirect("detail", pk=tal_result.pk) #name, body 끌고 오는것 

        #form에 기본 작성자 email을 로그인한 세션 유저를 기본으로 할당 
    else:
        comment_form=CommentForm() #내용물이 없는 것을 읽음    

    return render(request, 'tal_detail.html', {'tal_detail': tal_result,'comments':comments,'comment_form':comment_form})

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
        #list() : ListModelMixin에서 제공
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
        #list() : ListModelMixin에서 제공
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
    
#0809 삭제
# self.request.query_params는 Django REST Framework에서 HTTP 요청(request)의 쿼리 매개변수(query parameters)에 접근하는 방법 중 하나입니다. HTTP 요청은 URL에 추가적인 데이터를 전달하기 위해 쿼리 매개변수를 사용할 수 있습니다. 예를 들어, /your/api/endpoint/?post=post_id와 같은 URL에서 post=post_id가 쿼리 매개변수입니다.

# self.request는 현재 요청(request)에 대한 정보를 가지고 있는 객체입니다. self.request.query_params를 사용하면 해당 요청의 쿼리 매개변수에 접근할 수 있습니다.

# self.request.query_params.get('post', None)는 post라는 키(key)를 가진 쿼리 매개변수의 값을 가져오는 코드입니다. get() 메서드는 딕셔너리(dict)에서 특정 키의 값을 가져오는 메서드로, 첫 번째 인수로 찾고자 하는 키를 전달하고, 두 번째 인수로 해당 키가 존재하지 않을 때 반환할 기본값(default value)을 지정할 수 있습니다.

# 위의 코드에서는 post라는 키의 값을 가져오려고 하고, 만약 해당 키가 존재하지 않는다면 기본값으로 None을 지정하였습니다. 따라서 post라는 키의 값을 가져올 수 있으면 해당 값이 변수 post_id에 저장되고, 키가 존재하지 않으면 post_id는 None이 될 것입니다.
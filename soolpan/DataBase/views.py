from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tal
from .forms import DetailForm, CommentForm
import random
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

def index_v1(request):
    tals = Tal.objects.all()
    if request.method == 'POST':
        form = DetailForm(request.POST)
        if form.is_valid():
            search_query = request.POST.get('search_query')
            if search_query:
                try:
                    search = Tal.objects.get(name__icontains=search_query)
                    return redirect('detail', pk=search.pk)
                except:
                    form.add_error('name', '해당하는 술을 찾을 수 없습니다.')
    else:
        form=DetailForm()
    return render(request, 'index.html', {'tals':tals, 'form':form})

def tal_detail(request, pk):
    tal_result =  get_object_or_404(Tal,pk=pk)

     #pk=pk인 대상의 정보들을 가져오거나 404
    comments = tal_result.comments.all() #rel_name comments, 관련된 Comments의 post(rel_name=comments) 값들을 모두 가져온 것을 comments로 해라
    #이부분 중요
    #rel_name=comments는 Post 모델에서 Comment 모델과의 ForeignKey로 연결된 역참조 매니저
    #역참조 매니저를 사용하면 Post 객체와 연결된 모든 댓글 객체를 쿼리셋으로 가져올 수 있음
    #ForeignKey를 사용하여 모델을 연결하면, 연결된 객체들의 역참조 매니저가 자동으로 생성,
    #역참조 매니저는 related_name 매개변수를 사용하여 사용자 정의 이름으로 지정
    #Post 모델과 연결된 모든 댓글을 가져올 때 comments 속성을 사용
    #post.comments.all()은 post 변수에 할당된 Post 객체와 연결된 모든 댓글 객체들을 가져오는 코드
    # related_name 은 포스트(글)이 데리고 있는 모든 댓글들을 불러오는 참조 방식이다. 

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) #커밋을 완료하면 수정삭제가 안됨
            #Commit=false : db안에 즉시 저장하지 말고 객체를 반환하여 수정을 허용
            comment.post = tal_result
            comment.save()
            return redirect("detail", pk=tal_result.pk) #name, body 끌고 오는것 
    else:
        comment_form=CommentForm() #내용물이 없는 것을 읽음
    

    return render(request, 'tal_detail.html', {'tal_detail': tal_result,'comments':comments,'comment_form':comment_form})

# 이건 작동 안함
# class TalDetail(DetailView):
#         template_name="tal_detail.html" #여따가 딱뿌려
#         context_object_name = 'tal_detail' #이름은 Product
#         queryset = Tal.objects.get(pk=pk) #DB에서 싹 가져와서 


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import Truncator
from .models import Post
from .forms import PostForm
from django.http import Http404
from django.core.paginator import Paginator
from spUser.models import SpUser
# Create your views here.
# Post데이터 베이스의 모든 데이터 가져오기(published_date가 현재시간기준 이전시간꺼 모두 가져오기)
# publiShed_date__lte: 여기서 lte는 "less than or equal to"의 약자로,
# 이는 publiShed_date 필드 값이 지정된 값보다 작거나 같은 객체를 필터링하겠다는 의미.

def post_list(request):    
    post=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    page = int(request.GET.get('p', 1))
    pagnator=Paginator(post, 6)
    posts = pagnator.get_page(page)    
    email = request.session.get('user')
   
    return render(request, "post_list.html", {"posts":posts, "email":email})

def post_new(request):
    if not request.session.get('user'):
        return redirect('/user/login/')
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session.get('user')
            bloguser = SpUser.objects.get(email=user_id)

            post = form.save(commit=False) 
            post.author = bloguser     #request.user : 로그인 했을 때 django에서 만들어주는 객체       
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)    
    else:
        form=PostForm()
        
    return render(request, 'post_new.html', {'form':form})

def post_detail(request, pk):
    try:
        posts = get_object_or_404(Post, pk=pk)
    except Post.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    email = request.session.get('user')

    return render(request, "post_detail.html", {'post':posts, "email":email})


def post_edit(request, pk):
    user_id = request.session.get('user')
    if not request.session.get('user'):
        return redirect('/user/login/')
    try:
        post = Post.objects.get(pk=pk) #유저 정보 관련된 객체만 집어옴        
    except Post.DoesNotExist:
        raise Http404("게시글을 찾을 수 없습니다.")
    
    if SpUser.objects.get(email=user_id) == post.author:
        if request.method=="POST": #포스트 방식이면
            form=PostForm(request.POST, request.FILES, instance=post) #유효성 검사내용 form에 저장
            if form.is_valid(): #form에 잘 들어오면         
                
                bloguser = SpUser.objects.get(email=user_id) 

                post = form.save(commit=False) 
                post.author = bloguser #작성자
                post.published_date = timezone.now()
                post.save() 
                return redirect("post_detail", pk=post.pk)
            
        else:
            form=PostForm(instance=post) #이거 안해주면 원래 가져온 게시물 내용을 
            #form=PostForm(initial={'title':post.title, 'text':post.text, 'image':post.image}, instance=post) #이거 안해주면 원래 가져온 게시물 내용을 
    else:
        raise Http404("권한이 없습니다.")
    return render(request, 'post_edit.html', {'form':form})

def post_delete(request, pk):
    user_id = request.session.get('user')
    if not request.session.get('user'):
        return redirect('user/login/')
    
    post = Post.objects.get(pk=pk) #유저 정보 관련된 객체만 집어옴
    
    if SpUser.objects.get(email=user_id) == post.author:
        post.delete()
    else:
        raise Http404("권한이 없습니다.")
    return redirect('post_list')
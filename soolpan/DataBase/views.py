from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Tal
from .forms import DetailForm
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
    tal_result = Tal.objects.get(pk=pk)
    return render(request, 'tal_detail.html', {'tal_detail': tal_result})

# 이건 작동 안함
# class TalDetail(DetailView):
#         template_name="tal_detail.html" #여따가 딱뿌려
#         context_object_name = 'tal_detail' #이름은 Product
#         queryset = Tal.objects.get(pk=pk) #DB에서 싹 가져와서 


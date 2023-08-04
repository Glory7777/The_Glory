from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Tal
import random
# Create your views here.
#홈화면 검색/Autocomplete 기능 구현
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

class TalDetail(DetailView):
        template_name="tal_detail.html" #여따가 딱뿌려
        context_object_name = 'tal_detail' #이름은 Product
        queryset = Tal.objects.all() #DB에서 싹 가져와서 

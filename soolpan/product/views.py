from django.shortcuts import render
from DataBase.models import Tal
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q

class ProductList(ListView):
    model = Tal
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 6  # 원하는 페이지당 아이템 수로 변경 가능

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

        context['search_query'] = self.request.GET.get('search_query', '')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(dsc__icontains=search_query)
            )
        
        return queryset
        
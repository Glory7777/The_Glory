from django.shortcuts import render
from .models import Book

def search_books(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            # 검색어를 사용하여 Book 모델에서 연관 항목 5개를 쿼리
            related_books = Book.objects.filter(name__icontains=search_query)[:10]
        else:
            related_books = []
    else:
        related_books = []

    return render(request, 'search.html', {'related_books': related_books})

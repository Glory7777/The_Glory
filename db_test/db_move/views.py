from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Book

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        try:
            book = Book.objects.get(name__icontains=search_query)
            return redirect('detail', pk=book.pk)
        except Book.DoesNotExist:
            pass
    return render(request, 'search1.html')

def detail_view(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'detail.html', {'book': book})
from django.shortcuts import render
from .models import Tal
import random
# Create your views here.
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


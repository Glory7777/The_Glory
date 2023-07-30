from django.shortcuts import render
from .models import Tal

def index(request):
    tals = Tal.objects.all()
    return render(request, 'ac.html', {'tals':tals})
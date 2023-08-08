from django.shortcuts import redirect
from .models import SpUser


def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')       
        return function(request, *args, **kwargs) 
    return wrap # @login_required

def Admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')  
        user = SpUser.objects.get(email=user)     
        if user.level != 'admin':
            return redirect('/')
        
        return function(request, *args, **kwargs) 
    return wrap # @login_required


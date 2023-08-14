from django.shortcuts import render
from DataBase.models import Tal
from django.views.generic import ListView

class ProductList(ListView):
    model = Tal
    template_name = 'product.html'
    context_object_name = 'product_list'
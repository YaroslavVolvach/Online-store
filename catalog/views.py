from django.shortcuts import render
from .models import *


def product_list (request):
    s = 'catalog_list'
    return render(request, 'catalog/product_list.html', context={'categories': Category.objects.all()})



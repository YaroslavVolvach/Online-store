from django.shortcuts import render
from .models import *


def product_list(request):
    return render(request, 'catalog/product_list.html', context={'categories': Category.objects.all()})



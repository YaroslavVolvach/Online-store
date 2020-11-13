from django.shortcuts import render, get_object_or_404

from django.views.generic.base import View
from .models import *


def product_list(request):
    context = {
        'categories': Category.objects.all(),
        'products' : Product.objects.all()}
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, id):
    return render(request, 'catalog/product_detail.html', context={'product': get_object_or_404(Product, id=id)})


def select_category(request, id):
    context = {'current_category': get_object_or_404(Category, id=id),
               'products': Product.objects.filter(category=id),
               'categories': Category.objects.all()}
    return render(request, 'catalog/product_list.html', context)

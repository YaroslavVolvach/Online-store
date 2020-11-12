from django.shortcuts import render, get_object_or_404
from .models import *


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', context={'categories': categories, 'products': products})


def product_detail(request, id):
    return render(request, 'catalog/product_detail.html', context={'product': get_object_or_404(Product, id=id)})




from django.shortcuts import render, get_object_or_404

from django.views.generic.base import View
from .models import *


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', context={'categories': categories, 'products': products})


def product_detail(request, id):
    return render(request, 'catalog/product_detail.html', context={'product': get_object_or_404(Product, id=id)})


class SelectCategory(View):
    def get(self, request, id):
        products = Product.objects.filter(category_id=id)
        categories = Category.objects.all()
        if products.first() is not None:
            return render(request, 'catalog/product_list.html', context={'categories': categories, 'products': products})
        else:
            pass
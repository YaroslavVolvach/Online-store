from django.shortcuts import render, get_object_or_404

from django.views.generic.base import View
from .models import *
from cart.forms import *
from django.core.paginator import Paginator
from django.db.models import Q


def product_list (request, category_id=False):
    if request.GET.get('search', ''):
        products = Product.objects.filter(
            Q(title__icontains=request.GET.get('search', '')) | Q(title__iexact=request.GET.get('search', '')))
    elif category_id:
        products = Product.objects.filter(category=get_object_or_404(Category, id=category_id))
    else:
        products = Product.objects.all()

    page = Paginator(products, 8).get_page(request.GET.get('page', 1))

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {'categories': Category.objects.all(), 'products': page, 'is_paginated': is_paginated,
               'prev_url': prev_url, 'next_url': next_url}
    if category_id:
        context['current_category'] = get_object_or_404(Category, id=category_id)
        context['products'] = Product.objects.filter(category=category_id)

    return render(request, 'catalog/product_list.html', context)


def product_detail (request, id):
    context = {
        'product': get_object_or_404(Product, id=id),
        'cart_product_form': CartAddProductForm(),

    }
    return render(request, 'catalog/product_detail.html', context)

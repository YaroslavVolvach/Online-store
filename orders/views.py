from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm
from catalog.models import Product


def order(request):
    if request.method == 'POST':
        if OrderForm(request.POST).is_valid():

            OrderForm(request.POST).save(Cart(request))

            return redirect('catalog:product_list')
    else:

        return render(request, 'detail.html', context={'form': OrderForm()})

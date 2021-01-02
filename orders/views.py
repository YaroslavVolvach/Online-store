from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm


def order(request):
    if request.method == 'POST':
        if OrderForm(request.POST).is_valid():
            OrderForm(request.POST).save(Cart(request))

            return redirect('catalog:product_list')

    return render(request, 'detail.html', {'form': OrderForm()})

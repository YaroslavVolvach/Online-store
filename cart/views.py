from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .cart import Cart
from .forms import CartAddProductForm
from catalog.models import Product


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    quantity = product.quantity + 1
    form = CartAddProductForm(quantity, request.POST)
    if form.is_valid():
        cart.add(product=product,
                 quantity=form.cleaned_data['quantity'],
                 update_quantity=form.cleaned_data['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    Cart(request).remove(str(product_id))
    messages.success(request, 'Удалено')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True}, choices=item['product_quantity'] + 1)
    return render(request, 'cart/detail.html', {'cart': cart})

from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from catalog.models import Product


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            my_order = Order.objects.create(name=form.cleaned_data['name'],
                                            family_name=form.cleaned_data['family_name'],
                                            city=form.cleaned_data['city'],
                                            number_phone=form.cleaned_data['number_phone'],
                                            postcode=form.cleaned_data['postcode'])

            cart = Cart(request)
            list_item = []
            total_cost = 0
            for item in cart:
                list_item.append(OrderItem.objects.create(product=item['product'], price=item['price'],
                                                          quantity=item['quantity'], total_price=item['total_price']))

                product = Product.objects.get(id=item['product_id'])
                product.quantity = product.quantity - item['quantity']
                product.save()
                total_cost += item['total_price']

            cart.clear()

            my_order.items.set(list_item)
            my_order.total_cost = total_cost
            my_order.save()

            return redirect('catalog:product_list')
    else:
        return render(request, 'detail.html', context={'form': OrderForm()})

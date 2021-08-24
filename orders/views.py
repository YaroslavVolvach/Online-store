from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem


def order(request):
    form = OrderForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save(Cart(request), user=request.user)

        return redirect('catalog:product_list')

    return render(request, 'detail.html', {'form': OrderForm()})


class OrderList(ListView):
    model = Order
    page_kwarg = 10
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user__id=self.kwargs.get('user_id'))


def order_detail(request, order_id):
    current_order = get_object_or_404(Order, id=order_id)
    order_dict = {'Name': current_order.name,
                  'Family name': current_order.family_name,
                  'City': current_order.city,
                  'Postcode': current_order.postcode,
                  'id': current_order.id,
                  'Total price': current_order.total_cost}

    items = OrderItem.objects.filter(order=current_order)
    return render(request, 'items.html', {'items': items, 'info': order_dict})
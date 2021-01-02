from .models import Order, OrderItem
from django import forms
from catalog.models import Product


class OrderForm(forms.Form):
    name = forms.CharField(label='Имя')
    family_name = forms.CharField(label='Фамилия', )
    city = forms.CharField(label='Город')
    number_phone = forms.IntegerField(label='Номер телефона')
    postcode = forms.IntegerField(label='Почтовый индекс')

    name.widget.attrs.update({'class': 'form-control'})
    family_name.widget.attrs.update({'class': 'form-control'})
    city.widget.attrs.update({'class': 'form-control'})
    number_phone.widget.attrs.update({'class': 'form-control'})
    postcode.widget.attrs.update({'class': 'form-control'})

    def save(self, cart):
        my_order = Order(
            name=self.cleaned_data['name'],
            family_name=self.cleaned_data['family_name'],
            city=self.cleaned_data['city'],
            number_phone=self.cleaned_data['number_phone'],
            postcode=self.cleaned_data['postcode'],
        )

        my_order.total_cost = cart.get_total_price()

        my_order.save()

        for item in cart:
            OrderItem.objects.create(product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'],
                                     total_price=item['total_price'],
                                     order=my_order)

            product = Product.objects.get(id=item['product_id'])
            product.quantity = product.quantity - item['quantity']
            product.save()

        cart.clear()

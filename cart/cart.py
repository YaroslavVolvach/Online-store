from decimal import Decimal
from django.conf import settings
from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def add(self, product, quantity, update_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] > product.quantity:
            self.cart[product_id]['quantity'] = product.quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        products_keys = self.cart.keys()
        products = Product.objects.filter(id__in=products_keys)
        for product in products:
            self.cart[str(product.id)]['product'] = product
            self.cart[str(product.id)]['product_id'] = product.id

        for item in self.cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

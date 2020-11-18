from .cart import Cart
from catalog.views import product_detail


def cart(request):
    # возвращаем словарь, который будет отображаться во всех шаблонах
    return {'cart': Cart(request)}
from django.urls import path

from .views import order

app_name = 'orders'

urlpatterns = [
    path('', order, name='order')
]

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('list/<int:user_id>/', views.OrderList.as_view(), name='order_list'),
    path('items/<int:order_id>/', views.order_detail, name='order_detail')
]

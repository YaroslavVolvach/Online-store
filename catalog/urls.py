from django.urls import path
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:category_id>', product_list, name='select_category'),
    path('<int:id>/', product_detail, name='product_detail')]

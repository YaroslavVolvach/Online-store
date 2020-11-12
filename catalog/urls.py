from django.urls import path
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', product_list),
    path('<int:id>/', product_detail, name='product_detail')]

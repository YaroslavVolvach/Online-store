from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:category_id>', views.product_list, name='select_category'),
    path('<int:id>/', views.product_detail, name='product_detail')]

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('category/<int:id>', views.SelectCategory.as_view(), name='select_category')]

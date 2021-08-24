from django.urls import path
from . import views
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import CategoryCreationForm
from .models import Category
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<int:category_id>', views.ProductList.as_view(), name='select_category'),
    path('product_create', views.ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:product_id>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('category_create/', CreateView.as_view(
        form_class=CategoryCreationForm,
        model=Category,
        success_url=reverse_lazy('catalog:product_list'),
        template_name='catalog/category_create.html'
    ), name='category_create'),
    path('category_update/<int:id>', UpdateView.as_view(
        context_object_name='up_category',
        form_class=CategoryCreationForm,
        model=Category,
        pk_url_kwarg='id',
        success_url=reverse_lazy('catalog:product_list'),
        template_name='catalog/category_create.html'
    ), name='category_update'),
    path('category_delete/<int:id>', views.category_delete, name='category_delete'),
    path('category_admin/', ListView.as_view(
        context_object_name='categories',
        model=Category,
        queryset=Category.objects.all(),
        template_name='catalog/category_admin.html'
    ), name='category_admin'),
    path('comment_create/<int:user_id>/<int:product_id>/', views.comment_create, name='comment_create'),
    path('comment_edit/<int:comment_id>/<int:product_id>/', views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:comment_id>/<int:product_id>/', views.comment_delete, name='comment_delete'),
    path('like/<int:comment_id>/<int:product_id>/', views.like, name='like'),
    path('unlike/<int:like_id>/<int:product_id>/', views.unlike, name='unlike')]

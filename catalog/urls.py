from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'catalog'

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    # path('<int:category_id>', views.product_list, name='select_category'),
    path('', views.ProductList.as_view(), name='product_list'),
    path('<int:category_id>', views.ProductList.as_view(), name='select_category'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('comment_create/<int:user_id>/<int:product_id>/', views.comment_create, name='comment_create'),
    path('comment_edit/<int:comment_id>/<int:product_id>/', views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:comment_id>/<int:product_id>/', views.comment_delete, name='comment_delete'),
    path('like/<int:comment_id>/<int:product_id>/', views.like, name='like'),
    path('unlike/<int:like_id>/<int:product_id>/', views.unlike, name='unlike')]

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Product, Category, Comment, Like
from django.core.paginator import Paginator
from account.models import CustomUser
from django.utils import timezone


class ProductList(ListView):
    model = Product
    page_kwarg = 12
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'

    def get_queryset(self):
        product_queryset = Product.objects.all()
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            product_queryset = Product.objects.filter(category=category_id)
        return product_queryset

    def get_context_data(self, **kwargs):
        id_ = self.kwargs.get('category_id')
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if id_ is not None:
            context['current_category'] = get_object_or_404(Category, id=id_)
        return context


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    context = {'product': product,
               'cart_product_form':  CartAddProductForm(choices=product.quantity + 1),
               'comments': product.comment.all()}

    return render(request, 'catalog/product_detail.html', context)


def comment_create(request, user_id, product_id):
    if request.user.is_active:
        Comment.objects.create(product=get_object_or_404(Product, id=product_id),
                               user=get_object_or_404(CustomUser, id=user_id),
                               text=request.POST.get('text'))
    return redirect('catalog:product_detail', id=product_id)


def comment_edit(request, comment_id, product_id):
    edit_comment = get_object_or_404(Comment, id=comment_id)
    if request.user is edit_comment.user:
        edit_comment.text = request.POST.get('text')
        edit_comment.edit_joined = timezone.now()
        edit_comment.save()
    return redirect('catalog:product_detail', id=product_id)


def comment_delete(request, comment_id, product_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user is request.user or request.user.is_staff:
        comment.delete()
    return redirect('catalog:product_detail', id=product_id)


def like(request, comment_id, product_id):
    if request.user.is_active:
        Like.objects.create(comment=get_object_or_404(Comment, id=comment_id),
                            user=request.user)

    return redirect('catalog:product_detail', id=product_id)


def unlike(request, like_id, product_id):
    like_ = get_object_or_404(Like, id=like_id)
    if request.user is like.user:
        like_.delete()
    return redirect('catalog:product_detail', id=product_id)


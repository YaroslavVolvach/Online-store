from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Product, Category, Comment, Like
from django.core.paginator import Paginator
from account.models import CustomUser
from django.utils import timezone

# def product_list(request, category_id=False):
#     if request.GET.get('search', ''):
#         products = Product.objects.filter(
#             Q(title__icontains=request.GET.get('search', ''))
#             | Q(title__iexact=request.GET.get('search', '')))
#     elif category_id:
#         products = Product.objects.filter(
#             category=get_object_or_404(Category, id=category_id))
#     else:
#         products = Product.objects.all()
#
#     page = Paginator(products, 8).get_page(request.GET.get('page', 1))
#
#     is_paginated = page.has_other_pages()
#
#     if page.has_previous():
#         prev_url = '?page={}'.format(page.previous_page_number())
#     else:
#         prev_url = ''
#
#     if page.has_next():
#         next_url = '?page={}'.format(page.next_page_number())
#     else:
#         next_url = ''
#
#     context = {'categories': Category.objects.all(),
#                'products': page,
#                'is_paginated': is_paginated,
#                'prev_url': prev_url,
#                'next_url': next_url}
#
#     if category_id:
#         context['current_category'] = get_object_or_404(
#             Category, id=category_id)
#
#         context['products'] = Product.objects.filter(category=category_id)
#
#     return render(request, 'catalog/product_list.html', context)


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
    cart_product_form = CartAddProductForm(choices=product.quantity + 1)

    context = {'product': product,
               'cart_product_form': cart_product_form,
               'comments': product.comment.all()}

    return render(request, 'catalog/product_detail.html', context)


def comment_create(request, user_id, product_id):
    Comment.objects.create(product=get_object_or_404(Product, id=product_id),
                           user=get_object_or_404(CustomUser, id=user_id),
                           text=request.POST.get('text'))
    return redirect('catalog:product_detail', id=product_id)


def comment_edit(request, comment_id, product_id):
    edit_comment = get_object_or_404(Comment, id=comment_id)
    edit_comment.text = request.POST.get('text')
    edit_comment.edit_joined = timezone.now()
    edit_comment.save()
    return redirect('catalog:product_detail', id=product_id)


def comment_delete(request, comment_id, product_id):
    get_object_or_404(Comment, id=comment_id).delete()
    return redirect('catalog:product_detail', id=product_id)


def like(request, comment_id, product_id):
    Like.objects.create(comment=get_object_or_404(Comment, id=comment_id),
                        user=request.user)

    return redirect('catalog:product_detail', id=product_id)


def unlike(request, like_id, product_id):
    print()
    print(like_id)
    print()
    get_object_or_404(Like, id=like_id).delete()
    return redirect('catalog:product_detail', id=product_id)


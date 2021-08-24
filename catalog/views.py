from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from .mixins import ProductCreateUpdateMixin
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Product, Gallery, Category, Comment, Like
from django.core.paginator import Paginator
from account.models import CustomUser
from django.utils import timezone
from .forms import GalleryForm, CategoryCreationForm
from django.contrib.admin.views.decorators import staff_member_required


class ProductList(ListView):
    model = Product
    page_kwarg = 12
    template_name = 'catalog/product_list.html'

    def get_context_data(self, **kwargs):
        visit = self.request.session.get('visit', 0)
        self.request.session['visit'] = visit + 1
        category_id = self.kwargs.get('category_id')
        context = {
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'visit': visit
        }
        if category_id is not None:
            category = get_object_or_404(Category, id=category_id)
            context['current_category'] = category
            context['products'] = category.products.all()
        return context


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {'product': product,
               'cart_product_form':  CartAddProductForm(choices=product.quantity + 1),
               'comments': product.comment.all()}

    return render(request, 'catalog/product_detail.html', context)


class ProductCreateView(ProductCreateUpdateMixin):
    pass


class ProductUpdateView(ProductCreateUpdateMixin):

    def get_form_kwargs(self):
        self.kwargs['product'] = get_object_or_404(
                                             Product,
                                             id=self.kwargs.get('product_id')
        )
        return self.kwargs

    def get(self, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        return super().get(*args, *kwargs)

    def post(self, *args, **kwargs):
        kwargs = self.get_form_kwargs()
        return super().post(*args, *kwargs)


@staff_member_required(login_url='catalog:product_list')
def product_delete(request, product_id):
    get_object_or_404(Product, id=product_id).delete()
    return redirect('catalog:product_list')


def comment_create(request, user_id, product_id):
    if request.user.is_active:
        Comment.objects.create(product=get_object_or_404(Product, id=product_id),
                               user=get_object_or_404(CustomUser, id=user_id),
                               text=request.POST.get('text'))
    return redirect('catalog:product_detail', product_id)


def comment_edit(request, comment_id, product_id):
    edit_comment = get_object_or_404(Comment, id=comment_id)
    if request.user is edit_comment.user:
        edit_comment.text = request.POST.get('text')
        edit_comment.edit_joined = timezone.now()
        edit_comment.save()
    return redirect('catalog:product_detail', product_id)


def comment_delete(request, comment_id, product_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user is request.user or request.user.is_staff:
        comment.delete()
    return redirect('catalog:product_detail', product_id)


def like(request, comment_id, product_id):
    if request.user.is_active:
        Like.objects.create(comment=get_object_or_404(Comment, id=comment_id),
                            user=request.user)

    return redirect('catalog:product_detail', product_id)


def unlike(request, like_id, product_id):
    like_ = get_object_or_404(Like, id=like_id)
    if request.user is like.user:
        like_.delete()
    return redirect('catalog:product_detail', product_id)


@staff_member_required(login_url='catalog:product_list')
def category_delete(request, id):
    get_object_or_404(Category, id=id).delete()
    return redirect('catalog:product_list')





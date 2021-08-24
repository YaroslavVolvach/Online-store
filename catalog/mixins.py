from django.views.generic import View
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Product, Gallery
from .forms import ProductCreationForm, GalleryForm


class ProductCreateUpdateMixin(View):
    formset_class = inlineformset_factory(
        Product,
        Gallery,
        form=GalleryForm,
        fields=('image',),
        min_num=2,
        extra=1
        )

    def get(self, *args, **kwargs):
        product = self.kwargs.get('product')
        context = {
            'form': ProductCreationForm(instance=product),
            'formset': self.formset_class(instance=product),
            'product': product
        }
        return render(self.request, 'catalog/product_create.html', context)

    def form_valid(self, product):
        formset = self.formset_class(
            self.request.POST,
            self.request.FILES,
            instance=product
                                     )
        if formset.is_valid():
            formset.save()
            if self.request.POST.get('add') is not None:
                return redirect('catalog:product_update', product.id)

        return redirect('catalog:product_list')

    def post(self, *args, **kwargs):
        product = self.kwargs.get('product')
        form = ProductCreationForm(self.request.POST, self.request.FILES, instance=product)

        if form.is_valid():
            return self.form_valid(form.save())
        else:
            context = {'product_creation_errors': form.errors}
            return render(self.request, 'catalog/product_create.html', context)
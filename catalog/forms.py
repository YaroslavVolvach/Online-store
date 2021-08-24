from django import forms
from .models import Product, Gallery, Category
from .widgets import ImageWidget
from django.forms.widgets import TextInput


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(widget=ImageWidget(), required=False, label='')

    class Meta:
        model = Gallery
        fields = ('image',)


class ProductCreationForm(forms.ModelForm):
    image = forms.ImageField(widget=ImageWidget(), required=False)

    class Meta:
        model = Product
        fields = (
            'title', 'description', 'price', 'quantity', 'category', 'image'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}


class CategoryCreationForm(forms.ModelForm):
    title = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control'}),
         )

    class Meta:
        model = Category
        fields = ('title',)
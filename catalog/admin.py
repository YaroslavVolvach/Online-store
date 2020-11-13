from django.contrib import admin
from .models import *


admin.site.register(Category)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'image')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'category', 'description', 'price', 'quantity', 'actual')

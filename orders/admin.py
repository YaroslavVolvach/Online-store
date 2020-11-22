from django.contrib import admin

from .models import Order, OrderItem


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fk = 'order'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'family_name', 'city', 'number_phone', 'postcode', 'total_cost']

    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
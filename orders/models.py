from django.db import models
from django.urls import reverse
from account.models import CustomUser


class Order(models.Model):
    name = models.CharField(max_length=15)
    family_name = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    number_phone = models.PositiveIntegerField()
    postcode = models.PositiveIntegerField()
    total_cost = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.deletion.CASCADE,
                             related_name='my_orders', null=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_absolute_url (self):
        return reverse('orders:order_detail', args=[self.id])

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.deletion.CASCADE,
                              related_name='items', null=True)

    def __str__(self):
        return self.product

from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=15)
    family_name = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    number_phone = models.PositiveIntegerField()
    postcode = models.PositiveIntegerField()
    total_cost = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.deletion.CASCADE, related_name='items')

    def __str__(self):
        return self.product

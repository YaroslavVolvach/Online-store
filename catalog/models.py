from django.db import models
from django.urls import reverse
from django.utils import timezone
from account.models import CustomUser


class Category(models.Model):
    title = models.CharField('Категория', max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('catalog:select_category', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(verbose_name='Название товара', max_length=20)
    image = models.ImageField(verbose_name='Главное фото',
                              upload_to='product_image/product_photo/main_photo/',
                              default='product_image/default_image/default-no-image.png')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 null=True)
    description = models.TextField(verbose_name='Описание товара',
                                   max_length=1000)
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    product = models.ForeignKey(Product, null=True, verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(verbose_name='Фотография',
                              upload_to='product_image/product_photo/')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = 'Фото к товару'
        verbose_name_plural = 'Фотографии к товару'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comment')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='comment')
    text = models.TextField(max_length=1000)
    date_joined = models.DateTimeField(default=timezone.now)
    edit_joined = models.DateTimeField(null=True)


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='like')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='like')

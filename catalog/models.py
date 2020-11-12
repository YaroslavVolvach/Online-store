from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категория', max_length=150, unique=True)
    description = models.TextField('Описание', blank=True)
    url = models.SlugField(verbose_name=160, unique=True)

    def __str__ (self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    image = models.ImageField(verbose_name='Главное фото', upload_to='main_photo/', blank=True)
    name = models.TextField(verbose_name='Название товара', max_length=20)
    description = models.TextField(verbose_name='Описание товара', max_length=1000)
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    actual = models.BooleanField(verbose_name='В наличии', help_text='Если товар не набросок, то ставить галочку')
    url = models.SlugField(max_length=160, unique=True)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id])
        # return reverse('product_detail', kwargs={'slug': self.url})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ImageProduct(models.Model):
    title = models.TextField(verbose_name='Название', max_length=100)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фотография', upload_to='product_photo/')

    class Meta:
        verbose_name = 'Фото к товару'
        verbose_name_plural = 'Фотографии к товару'

    def __str__ (self):
        return self.title


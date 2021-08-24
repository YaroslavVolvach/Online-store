from django.test import TestCase


from catalog.models import Product, Category, Gallery


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

       product = Product.objects.create(
            title='Submariner',
            description='Nice',
            price=1000,
            quantity=10
        )
       Category.objects.create(title="Rolex", products=product)
       Gallery.objects.create(
           product=product,
           image='product_image/default_image/default-no-image.png'
       )

    def test_product_str_method(self):
        product = Product.objects.get(id=1)
        self.assertEquals(product.__str__(), product.title)

    def test_category_str_method(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.__str__(), category.title)

    def test_gallery_str_method(self):
        gallery = Gallery.objects.get(id=1)
        self.assertEquals(gallery.__str__(), str(gallery.image))

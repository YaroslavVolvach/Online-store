from django.test import RequestFactory, TestCase
from catalog import views, models
from django.urls import reverse
from cart.forms import CartAddProductForm
from django.contrib.admin.views.decorators import staff_member_required
from account.models import CustomUser
from catalog import views


class CreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for number in range(1, 11):
           product = models.Product.objects.create(
                title='Product:{}'.format(number),
                description='Nice',
                price=1000,
                quantity=10
            )
           category =models.Category.objects.create(
               title="Category:{}".format(number),
           )
           category.products.set([product])
           models.Gallery.objects.create(
                product=product,
                image='product_image/default_image/default-no-image.png'
            )


class ProductListViewTest(CreateViewTest):
    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(self.client.get('').status_code, 200)

    def test_view_url_exists_at_accessible_by_name(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        self.assertTemplateUsed((self.client.get(''), 'catalog/product_list.html'))

    def test_view_list(self):
        all_product_ = self.client.get('').context['products']
        all_product = models.Product.objects.all()
        self.assertEqual(all_product_.__class__, all_product.__class__)
        self.assertEqual(all_product_.count(), all_product.count())

    def test_view_category_list(self):
        all_categories_list = self.client.get('').context['categories'].count()
        all_categories_count = models.Category.objects.all().count()
        self.assertEqual(all_categories_list, all_categories_count)


class ProductDetailViewTest(CreateViewTest):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/product_detail/9')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_accessible_by_name(self):
        response = self.client.get(reverse('catalog:product_detail', args=[8]))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get('/product_detail/7')
        self.assertTemplateUsed(response, 'catalog/product_detail.html')

    def test_context_view(self):
        response = self.client.get('/product_detail/6')
        product = models.Product.objects.get(id=6)
        self.assertEqual(response.context['product'], product)

    def test_form_view(self):
        response = self.client.get('/product_detail/6')
        form_class = response.context['cart_product_form'].__class__
        self.assertEqual(form_class, CartAddProductForm)

    def test_comment_view(self):
        response = self.client.get('/product_detail/4')
        product = models.Product.objects.get(id=4)
        comments = response.context['comments']
        self.assertQuerysetEqual(comments, product.comment.all())


class ProductDeleteTest(TestCase):
    def setUp(self):
        self.product = models.Product.objects.create(
            title='Watch',
            description='Nice',
            price=1000,
            quantity=10
        )
        self.user = CustomUser.objects.create_user(
            email='product_delete_test@gmail.com',
            password='secret',
            user_name='ProductDeleteTest'
        )

    def test_delete_view(self):
        response = self.client.get('/product_delete/3/')

        self.assertTrue(models.Product.objects.filter(id=self.product.id).exists())
        self.assertRedirects(response, '/?next=%2Fproduct_delete%2F3%2F', 302, 200)

    def test_delete_view_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('catalog:product_delete', args=[3]))

        self.assertFalse(models.Product.objects.filter(id=self.product.id).exists())
        self.assertRedirects(response, '/', 302, 200)


class CommentViewTest(TestCase):
    @classmethod
    def setUpTestData (cls):
        cls.product = models.Product.objects.create(
            title='Watch',
            description='Nice',
            price=1000,
            quantity=10
        )
        cls.user = CustomUser.objects.create_user(
            email='product_delete_test@gmail.com',
            password='secret',
            user_name='ProductDeleteTest'
        )

    def setUp(self):
        self.comment = models.Comment.objects.create(
            product=self.product,
            user=self.user,
            text='Comment for Django test'
        )

    def test_comment_create_for_anonymous_user(self):
        comment_count = models.Comment.objects.all().count()
        response = self.client.post(
            reverse('catalog:comment_create',
                    args=[self.user.id, self.product.id]),
            {'text': 'Test'}
        )
        create_by_anonymous = models.Comment.objects.all().count()

        self.assertFalse(create_by_anonymous > comment_count)
        self.assertRedirects(
            response,
            reverse('catalog:product_detail', args=[self.product.id]),
            302,
            200
        )

    def test_comment_create_for_authenticated_user(self):
        comment_count = models.Comment.objects.all().count()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('catalog:comment_create',
                    args=[self.user.id, self.product.id]),
            {'text': 'Test'}
        )
        create_by_anonymous = models.Comment.objects.all().count()

        self.assertTrue(create_by_anonymous > comment_count)
        self.assertRedirects(
            response,
            reverse('catalog:product_detail', args=[self.product.id]),
            302,
            200
        )












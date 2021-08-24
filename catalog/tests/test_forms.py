from django.test import TestCase

from catalog.forms import GalleryForm, ProductCreationForm, CategoryCreationForm
from catalog.models import Gallery, Product, Category
from catalog.widgets import ImageWidget
from django.forms.widgets import TextInput


def test_attrs(form):
    for field in form.fields.values():
        if field.widget.attrs != {'class': 'form-control'}:
            return False
    return True


class GalleryFormTest(TestCase):
    @classmethod
    def setUpTestData (cls):
        cls.form = GalleryForm()

    def test_field_label(self):
        self.assertEqual(self.form.fields['image'].label, '')

    def test_field_required(self):
        self.assertFalse(self.form.fields['image'].required)

    def test_field_widget(self):
        widget = self.form.fields['image'].widget
        self.assertEqual(widget.__class__, ImageWidget)

    def test_meta_model(self):
        self.assertEqual(self.form.Meta.model, Gallery)

    def test_meta_model_field(self):
        self.assertEqual(self.form.Meta.fields, ('image',))


class ProductCreationFormTest(TestCase):
    @classmethod
    def setUpTestData (cls):
        cls.form = ProductCreationForm()

    def test_field_label(self):
        self.assertTrue(self.form.fields['image'].label is None)

    def test_field_required (self):
        self.assertFalse(self.form.fields['image'].required)

    def test_image_widget(self):
        widget = self.form.fields['image'].widget
        self.assertEqual(widget.__class__, ImageWidget)

    def test_attrs_widget(self):
        self.assertTrue(test_attrs(self.form))

    def test_meta_model(self):
        self.assertEqual(self.form.Meta.model, Product)

    def test_meta_model_field(self):
        meta_fields = ('title', 'description', 'price', 'quantity', 'category', 'image')
        self.assertEqual(self.form.Meta.fields, meta_fields)


class CategoryCreationFormTest(TestCase):
    @classmethod
    def setUpTestData (cls):
        cls.form = CategoryCreationForm()

    def test_field_label(self):
        self.assertTrue(self.form.fields['title'].label is None)

    def test_field_required (self):
        self.assertTrue(self.form.fields['title'].required)

    def test_image_widget(self):
        widget = self.form.fields['title'].widget
        self.assertEqual(widget.__class__, TextInput)

    def test_attrs_widget(self):
        self.assertTrue(test_attrs(self.form))

    def test_meta_model(self):
        self.assertEqual(self.form.Meta.model, Category)

    def test_meta_model_field(self):
        self.assertEqual(self.form.Meta.fields, ('title',))

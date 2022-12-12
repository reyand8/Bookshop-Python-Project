from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Category, Product


class TestCategotiesModel(TestCase):

    def setUp(self):
        self.init_data = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        data = self.init_data
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.init_data = Product.objects.create(category_id=1, title='django shop', created_by_id=1, slug='django-shop',
                                                price='12.00', image='django')

    def test_products_model_entry(self):
        data = self.init_data
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django shop')

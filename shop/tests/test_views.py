from importlib import import_module

from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from shop.models import Category, Product
from shop.views import product_all
from django.conf import settings


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory
        User.objects.create_user(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django shop', created_by_id=1,
                               slug='django-shop', price='12.00', image='django')

    def test_url_allowed_hosts(self):
        response = self.c.get('/', HTTP_HOST='0.1.1.1')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 400)

    def test_homepage_url(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        response = self.c.get(reverse('shop:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse('shop:product_detail', args=['django-shop']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    # def test_view_function(self):
    #     factory = RequestFactory()
    #     request = factory.get('/django')
    #     response = product_all(request)
    #     html = response.content.decode('utf8')
    #     self.assertIn('<title>Home</title>', html)
    #     self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
    #     self.assertEqual(response.status_code, 200)

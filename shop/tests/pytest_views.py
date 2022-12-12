from django.http import HttpRequest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from shop.models import Category, Product


@pytest.fixture()
def setup(client):
    Category.objects.create(name='newdjango', slug='newdjango')
    User.objects.create_user(username='admin')
    Product.objects.create(category_id=1, title='django shop', created_by_id=1,
                       slug='django-shop', price='12.00', image='django')


@pytest.mark.django_db
def test_homepage_url(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.usefixtures('setup')
@pytest.mark.django_db
def test_homepage_url(client):
    Category.objects.create(name='django', slug='django')
    url = reverse('shop:category_list', args=['django'])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_detail_url(client, setup):
    url = reverse('shop:product_detail', args=['django-shop'])
    response = client.get(url)
    assert response.status_code == 200



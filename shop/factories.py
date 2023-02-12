from django.contrib.auth.models import User
from shop.models import *
from faker import Faker
import factory
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    name = fake.name()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = 'django'
    slug = 'django'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(UserFactory)
    author = fake.name()
    title = fake.sentence()
    description = fake.text()
    image = fake.file_extension(category='image')
    price = fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=None, max_value=None)
    slug = fake.sentence()
    in_stock = fake.unique.boolean()
    is_active = fake.unique.boolean()
    created = fake.date()
    updated = fake.date()

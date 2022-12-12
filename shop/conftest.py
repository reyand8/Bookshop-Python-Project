from pytest_factoryboy import register
from shop.factories import *

register(UserFactory)
register(ProductFactory)
register(CategoryFactory)

from faker import Faker

fake = Faker()


def test_product_instance(db, product_factory):
    product = product_factory.create()
    print(product.price)
    assert True

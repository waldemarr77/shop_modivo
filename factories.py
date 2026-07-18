import factory
from django.contrib.auth import get_user_model
from catalog.models import Brand, MainCategory, SubCategory, Product
from inventory.models import Size, ProductVariant
from cart.models import Cart, CartItem

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Sequence(lambda n: f'user_{n}@modivo.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'Brand {n}')
    description = 'Тестовий бренд'


class MainCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MainCategory

    name = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')


class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Sequence(lambda n: f'SubCategory {n}')
    slug = factory.Sequence(lambda n: f'subcategory-{n}')
    main_category = factory.SubFactory(MainCategoryFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    description = 'Тестовий товар'
    price = 1000.00
    category = factory.SubFactory(SubCategoryFactory)
    brand = factory.SubFactory(BrandFactory)


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    name = factory.Sequence(lambda n: f'{40 + n}')


class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    size = factory.SubFactory(SizeFactory)
    stock = 10
    sku = factory.Sequence(lambda n: f'SKU-{n:04d}')


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    variant = factory.SubFactory(ProductVariantFactory)
    quantity = 1
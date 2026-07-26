import pytest
from assistant.tools import search_products_tool, check_order_status_tool
from factories import ProductFactory, BrandFactory
from orders.models import Order

@pytest.mark.django_db
def test_search_products_tool_found():
    brand = BrandFactory(name="Nike")
    ProductFactory(name="Кросівки Air Max", price=3000, brand=brand)
    
    result = search_products_tool.invoke({"query": "Кросівки"})
    
    assert "Ось що я знайшов" in result
    assert "Кросівки Air Max" in result
    assert "Nike" in result
    assert "3000" in result

@pytest.mark.django_db
def test_search_products_tool_not_found():
    result = search_products_tool.invoke({"query": "Нічого"})
    assert "На жаль, товарів за запитом 'Нічого' не знайдено." in result

@pytest.mark.django_db
def test_search_products_tool_with_price():
    brand = BrandFactory(name="Adidas")
    ProductFactory(name="Футболка Adidas 1", price=5000, brand=brand)
    ProductFactory(name="Футболка Adidas 2", price=2000, brand=brand)
    
    result = search_products_tool.invoke({"query": "Футболка", "max_price": 3000})
    
    assert "2000" in result
    assert "5000" not in result

@pytest.mark.django_db
def test_check_order_status_tool_found(django_user_model):
    user = django_user_model.objects.create_user(username="test_order", password="123")
    order = Order.objects.create(user=user, status='paid', address='Test addr')
    
    result = check_order_status_tool.invoke({"order_id": order.id})
    assert "Оплачено та готується до відправки" in result
    
@pytest.mark.django_db
def test_check_order_status_tool_not_found():
    result = check_order_status_tool.invoke({"order_id": 99999})
    assert "Замовлення з номером 99999 не знайдено в базі." in result

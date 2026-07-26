import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from factories import ProductFactory, BrandFactory


@pytest.mark.django_db
def test_product_list_returns_200(api_client):
    url = reverse('product-list')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_product(api_client):
    url = reverse('product-list')
    response = api_client.post(url, {})
    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_user_can_view_products(authenticated_client):
    url = reverse('product-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_products_by_brand(api_client):
    nike = BrandFactory(name='Nike')
    adidas = BrandFactory(name='Adidas')
    ProductFactory(brand=nike, name='Air Max')
    ProductFactory(brand=adidas, name='Ultraboost')

    url = reverse('product-list')
    response = api_client.get(url, {'brand': nike.id})

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Air Max'


@pytest.mark.django_db
def test_search_products_by_name(api_client):
    ProductFactory(name='Nike Air Max')
    ProductFactory(name='Adidas Ultraboost')

    url = reverse('product-list')

    with patch('catalog.views.get_redis_connection') as mock_redis:
        mock_redis.return_value = MagicMock()
        response = api_client.get(url, {'search': 'Nike'})

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert 'Nike' in response.data['results'][0]['name']


@pytest.mark.django_db
def test_ordering_products_by_price(api_client):
    ProductFactory(name='Cheap', price=500)
    ProductFactory(name='Expensive', price=5000)

    url = reverse('product-list')
    response = api_client.get(url, {'ordering': 'price'})

    assert response.status_code == 200
    prices = [p['price'] for p in response.data['results']]
    assert prices == sorted(prices)


@pytest.mark.django_db
def test_popular_searches_returns_200(api_client):
    url = reverse('popular-searches')

    with patch('catalog.views.get_redis_connection') as mock_redis:
        mock_conn = MagicMock()
        mock_redis.return_value = mock_conn
        mock_conn.zrevrange.return_value = [
            (b'nike', 42.0),
            (b'adidas', 31.0),
        ]
        response = api_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['query'] == 'nike'
    assert response.data[0]['count'] == 42
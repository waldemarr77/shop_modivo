import pytest
from django.urls import reverse

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
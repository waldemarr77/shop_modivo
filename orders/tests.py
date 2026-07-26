import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from factories import CartItemFactory, CartFactory, ProductVariantFactory


@pytest.mark.django_db
def test_unauthenticated_user_cannot_view_orders(api_client):
    url = reverse('order-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_user_can_view_own_orders(authenticated_client):
    url = reverse('order-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_with_empty_cart_returns_400(authenticated_client):
    url = reverse('checkout')
    response = authenticated_client.post(url, {'address': 'вул. Тестова 1'})
    assert response.status_code == 404


@pytest.mark.django_db
@patch('orders.views.stripe.checkout.Session.create')
@patch('orders.views.send_order_confirmation.delay')
def test_checkout_success(mock_send_mail, mock_stripe, authenticated_client, user):
    mock_stripe.return_value = MagicMock(url='http://fake.stripe.url')
    cart = CartFactory(user=user)
    variant = ProductVariantFactory(stock=10)
    CartItemFactory(cart=cart, variant=variant, quantity=2)

    url = reverse('checkout')
    response = authenticated_client.post(url, {'address': 'вул. Тестова 1'})

    assert response.status_code == 201
    assert response.data['order_id'] is not None
    variant.refresh_from_db()
    assert variant.stock == 8


@pytest.mark.django_db
def test_checkout_fails_when_stock_insufficient(authenticated_client, user):
    cart = CartFactory(user=user)
    variant = ProductVariantFactory(stock=1)
    CartItemFactory(cart=cart, variant=variant, quantity=5)

    url = reverse('checkout')
    response = authenticated_client.post(url, {'address': 'вул. Тестова 1'})

    assert response.status_code == 400
    assert 'error' in response.data
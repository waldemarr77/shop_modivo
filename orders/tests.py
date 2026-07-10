from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class OrderAPITest(APITestCase):
    def test_unauthenticated_user_cannot_view_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, CheckoutAPIView, StripeWebhookView

router = DefaultRouter()

router.register('order', OrderViewSet, basename='order')
router.register('order-item', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
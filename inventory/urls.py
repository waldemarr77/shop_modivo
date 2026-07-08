from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SizeViewSet, ProductVariantViewSet

router = DefaultRouter()

router.register('size', SizeViewSet, basename='size')
router.register('product-variant', ProductVariantViewSet, basename='product-variant')

urlpatterns = [
    path('', include(router.urls)),
]
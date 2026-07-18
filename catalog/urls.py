from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainCategoryViewSet, SubCategoryViewSet, BrandViewSet, ProductViewSet, PopularSearchesView

router = DefaultRouter()
router.register('main-category', MainCategoryViewSet, basename='main-category')
router.register('sub-category', SubCategoryViewSet, basename='sub-category')
router.register('brand', BrandViewSet, basename='brand')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('popular-searches/', PopularSearchesView.as_view(), name='popular-searches'),
]
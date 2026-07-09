from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import MainCategory, SubCategory, Brand, Product
from .serializers import MainCategorySerializer, SubCategorySerializer, BrandSerializer, ProductSerializer


class MainCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MainCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = MainCategory.objects.all()
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SubCategory.objects.all()
    

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Brand.objects.all()
    

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        cached = cache.get('product_list')

        if cached:
            return Response(cached)
        
        response = super().list(request, *args, **kwargs)

        cache.set('product_list', response.data, timeout=60*5)

        return response
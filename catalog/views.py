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
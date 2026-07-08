from rest_framework import viewsets
from .models import MainCategory, SubCategory, Brand, Product
from .serializers import MainCategorySerializer, SubCategorySerializer, BrandSerializer, ProductSerializer


class MainCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MainCategorySerializer
    queryset = MainCategory.objects.all()
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
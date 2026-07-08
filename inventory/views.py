from rest_framework import viewsets
from .models import Size, ProductVariant
from .serializers import SizeSerializer, ProductVariantSerializer


class SizeViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSerializer
    queryset = Size.objects.all()


class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
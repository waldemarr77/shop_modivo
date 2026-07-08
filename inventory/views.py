from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Size, ProductVariant
from .serializers import SizeSerializer, ProductVariantSerializer


class SizeViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Size.objects.all()


class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductVariant.objects.all()
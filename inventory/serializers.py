from rest_framework import serializers
from .models import Size, ProductVariant


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'stock', 'sku']
        read_only_fields = ['id', 'size', 'stock', 'sku']
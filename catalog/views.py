from datetime import date
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import MainCategory, SubCategory, Brand, Product
from .serializers import MainCategorySerializer, SubCategorySerializer, BrandSerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly


class MainCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MainCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = MainCategory.objects.all()


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = SubCategory.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Brand.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.select_related('brand', 'category').all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brand', 'category']
    search_fields = ['name', 'description', 'brand__name']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['name']

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', '').strip()
        if search_query:
            today = date.today().strftime('%Y-%m-%d')
            redis_key = f'popular_searches:{today}'
            redis_conn = get_redis_connection('default')
            redis_conn.zincrby(redis_key, 1, search_query)
            redis_conn.expire(redis_key, 60 * 60 * 48) 

        cache_key = f'product_list_{request.GET.urlencode()}'
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response


class PopularSearchesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = date.today().strftime('%Y-%m-%d')
        redis_key = f'popular_searches:{today}'
        redis_conn = get_redis_connection('default')

        top = redis_conn.zrevrange(redis_key, 0, 4, withscores=True)

        result = [
            {'query': item[0].decode('utf-8'), 'count': int(item[1])}
            for item in top
        ]

        return Response(result)
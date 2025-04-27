from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class MyPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class HomeAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description="Slug категории", type=openapi.TYPE_STRING),
        openapi.Parameter('subcategory', openapi.IN_QUERY, description="Slug подкатегории", type=openapi.TYPE_STRING),
        openapi.Parameter('sort', openapi.IN_QUERY, description="Фильтрации", type=openapi.TYPE_STRING),
    ])
    def get(self, request):
        category_slug = request.query_params.get('category')
        subcategory_slug = request.query_params.get('subcategory')
        sort = request.query_params.get('sort')

        category = Category.objects.all()
        products = Product.objects.all()

        if category_slug:
            products = products.filter(category__slug=category_slug)

        if subcategory_slug:
            products = products.filter(subcategory__slug=subcategory_slug)

        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'sale':
            products = products.filter(discount__isnull=False)
        elif sort == 'new':
            products = products.filter(status='new')
        elif sort == 'popular':
            products = products.filter(status='popular')

        paginator = MyPaginator()
        paginated_products = paginator.paginate_queryset(products, request)

        return paginator.get_paginated_response({
            'categories': CategorySerializer(category, many=True).data,
            'products': ProductSerializer(products, many=True).data
        })


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

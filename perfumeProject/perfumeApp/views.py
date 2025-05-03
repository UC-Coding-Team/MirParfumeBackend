from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .management.commands.bot import send_order_to_group


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


class ProductTelegramView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="Имя пользователя", type=openapi.TYPE_STRING),
        openapi.Parameter('phone_number', openapi.IN_QUERY, description="Телефон номер",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('product_slug', openapi.IN_QUERY, description="Slug товара", type=openapi.TYPE_STRING),
    ])
    def post(self, request):
        username = request.data.get("username")
        phone_number = request.data.get("phone_number")
        product_slug = request.data.get("product_slug")

        if not all([username, phone_number, product_slug]):
            return Response({"detail": "Все поля обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, slug=product_slug)

        async_to_sync(send_order_to_group)(username, phone_number, product.name)

        return Response(
            {"detail": "Успешно отправлено", 'username': username, 'phone_number': phone_number,
             'product': product.name},
            status=status.HTTP_200_OK)

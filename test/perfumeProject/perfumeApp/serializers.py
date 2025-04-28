from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'subcategories']

    def get_subcategories(self, category):
        subs = SubCategory.objects.filter(category=category)
        return SubCategorySerializer(subs, many=True).data


class OnlyCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class OnlySubCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    category = OnlyCategoryNameSerializer(read_only=True)
    subcategory = OnlySubCategoryNameSerializer(read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'images', 'category', 'subcategory', 'name', 'short_description', 'description', 'price',
            'discount',
            'final_price', 'status', 'slug', 'created_at')

    def get_final_price(self, product):
        if product.discount:
            procent = (product.price * product.discount) / 100
            price = product.price - procent
            return round(price)
        else:
            return product.price
        

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'phone', 'message', 'created_at']


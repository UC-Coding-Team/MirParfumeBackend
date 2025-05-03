from django.contrib import admin
from django.utils.safestring import mark_safe
from .forms import *
from .models import *
from modeltranslation.admin import TranslationAdmin


# Register your models here.
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'get_icon_admin'] 
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)} 
    form = CategoryForm

    def get_icon_admin(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30" />')
            except:
                return 'Нет иконки'
        else:
            return 'Нет иконки'

    get_icon_admin.short_description = 'Иконка'


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'icon', 'category', 'get_icon_admin']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
    form = SubCategoryForm

    def get_icon_admin(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30" />')
            except:
                return 'Нет иконки'
        else:
            return 'Нет иконки'

    get_icon_admin.short_description = 'Иконка'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['id', 'get_product_img', 'name', 'price', 'status', 'category']
    list_display_links = ['id', 'name', 'price', 'status']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    def get_product_img(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="50" />')
            except:
                return 'Нету изображения'
        else:
            return 'Нету изображения'

    get_product_img.short_description = 'Изображение продукта'

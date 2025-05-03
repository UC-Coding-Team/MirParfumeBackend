from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя категории')
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, verbose_name='Иконка категории')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя подкатегории')
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, verbose_name='Иконка подкатегории')
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',
                                 verbose_name='Выбор категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('popular', 'Популярный'),
    ]

    name = models.CharField(max_length=255, verbose_name='Имя товара')
    short_description = models.TextField(verbose_name='Короткое описание товара')
    description = models.TextField(verbose_name='Полное описание товара')
    price = models.IntegerField(verbose_name='Цена товара')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Скидка товара')
    volume = models.CharField(blank=True, null=True, verbose_name='Объем товара')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True,
                              verbose_name='Статус товара')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True,
                                 null=True, verbose_name='Категория товара')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_products', blank=True,
                                    null=True, verbose_name='Подкатегория товара')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class PendingOrders(models.Model):
    is_approve = models.BooleanField(default=False)
    message_id = models.IntegerField(blank=True, null=True)
    username = models.CharField()
    phone_number = models.CharField()
    slug = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ от {self.username}'

    class Meta:
        verbose_name = 'Товар в обработке'
        verbose_name_plural = 'Товары в обработке'

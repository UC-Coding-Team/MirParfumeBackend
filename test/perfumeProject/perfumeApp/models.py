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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True,
                              verbose_name='Статус товара')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория товара')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_products',
                                    verbose_name='Подкатегория товара')

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


from .utils.telegram import send_telegram_message

class ContactRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(blank=True, null=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            text = (
                f"<b>Новая заявка с сайта!</b>\n\n"
                f"👤 Имя: {self.name}\n"
                f"📞 Телефон: {self.phone}\n"
                f"📝 Сообщение: {self.message or 'Нет сообщения.'}"
            )
            send_telegram_message(text)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = 'Заявка на обратную связь'
        verbose_name_plural = 'Заявки на обратную связь'



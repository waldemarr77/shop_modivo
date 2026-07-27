from django.db import models
from pgvector.django import VectorField

class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, verbose_name='URL ідентифікатор')


    class Meta:
        ordering = ['name',]
        verbose_name = 'Головна категорія одягу'
        verbose_name_plural = 'Головні категорії одягу'

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Тип одягу')
    slug = models.SlugField(unique=True, verbose_name='URL ідентифікатор')
    main_category = models.ForeignKey(
        MainCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subcategories'
    )


    class Meta:
        verbose_name = 'Підкатегорія одягу'
        verbose_name_plural = 'Підкатегорії одягу'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Бренд')
    description = models.TextField()
    logo = models.ImageField(upload_to='logo/', null=True, blank=True, verbose_name='Лого бренду')


    class Meta:
        ordering = ['name',]
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Модель товару')
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Ціна')

    category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='product_category' 
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='brand_of_product'
    )

    image = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Фото товару')
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=384, null=True, blank=True)

    def get_semantic_text(self):
        return f"Бренд: {self.brand.name}. Назва: {self.name}. Опис: {self.description}"


    class Meta:
        ordering = ['name', 'price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return f'{self.brand} - {self.name} ({self.price})'

from django.db import models
from catalog.models import Product

class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name='Розмір')

    class Meta:
        ordering = ['-name',]
        verbose_name = 'Розмір'
        verbose_name_plural = 'Розміри'

    def __str__(self):
        return self.name
    

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='size_product'
    )

    stock = models.PositiveIntegerField(verbose_name='Кількість товару на складі')
    sku = models.CharField(max_length=20, unique=True, verbose_name='Артикул товару')


    class Meta:
        ordering = ['-stock',]
        unique_together = ['product', 'size']
        verbose_name = 'Варіант товару'
        verbose_name_plural = 'Варіанти товарів'

    def __str__(self):
        return f'{self.product} size {self.size} - {self.sku}'

from django.db import models
from users.models import CustomUser
from inventory.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('paid', 'Оплачено'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='order'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус замовлення')
    address = models.CharField(max_length=200, verbose_name='Адреса доставки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'{self.user} {self.status}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='item'
    ) 

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='product_item'
    )

    quantity = models.PositiveIntegerField(verbose_name='Кількість')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')


    class Meta:
        ordering = ['-price',]
        verbose_name = 'Замовлений товар'
        verbose_name_plural = 'Замовлені товари'

    def __str__(self):
        return f'{self.order} {self.variant}({self.quantity} шт.) - {self.price}'
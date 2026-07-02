from django.db import models
from users.models import CustomUser
from inventory.models import ProductVariant

class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')


    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'

    def __str__(self):
        return f'Кошик: {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_item'
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_variant'
    )

    quantity = models.PositiveIntegerField(verbose_name='Кількість')


    class Meta:
        ordering = ['-quantity',]
        unique_together = ['cart', 'variant']
        verbose_name = 'Замовлення в кошику'
        verbose_name_plural = 'Замовлення в кошиках'


    def __str__(self):
        return f'{self.cart}: {self.variant}'
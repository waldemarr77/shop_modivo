from django.db import models
from users.models import CustomUser
from catalog.models import Product

class Review(models.Model):
    CHOICES_RATING = [
        (1, 'Погано'),
        (2, 'Незадовільно'),
        (3, 'Задовільно'),
        (4, 'Добре'),
        (5, 'Відмінно'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Користувачі',
        related_name='user_review'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товари',
        related_name='review_product'
    )

    rating = models.PositiveSmallIntegerField(choices=CHOICES_RATING, verbose_name='Рейтинг')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at',]
        unique_together = ['user', 'product']
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

    def __str__(self):
        return f'Користувач {self.user}\nТовар {self.product}\nРейтинг {self.rating}'
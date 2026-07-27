from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('human', 'Human'),
        ('ai', 'AI'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Повідомлення чату'
        verbose_name_plural = 'Повідомлення чату'

    def __str__(self):
        return f'{self.user} [{self.role}]: {self.content[:50]}'

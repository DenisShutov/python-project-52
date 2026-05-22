from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя',
        error_messages={
            'unique': 'Статус с таким именем уже существует',
        }
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания')

    def __str__(self):
        return self.name
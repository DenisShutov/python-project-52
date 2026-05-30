from django.contrib.auth import get_user_model
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

# Create your models here.
User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя',
        error_messages={
            'unique': 'Задача с таким именем уже существует',
        }
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    executor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        verbose_name='Исполнитель'
    )

    labels = models.ManyToManyField(
        Label,
        verbose_name='Метки'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name
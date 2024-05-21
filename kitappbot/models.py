
from django.db import models
from django.utils import timezone

class TelegramGroup(models.Model):
    chatId = models.TextField(blank=False, verbose_name= "ID чата/группы")
    chatType = models.CharField(max_length=64, default='', verbose_name='Тип чата')

    def __str__(self) -> str:
        return f"{self.chatType}: {self.chatId}"

class TelegramSendedMessage(models.Model):
    text = models.TextField(blank=False, verbose_name= "Текст сообщения")
    receiver = models.CharField(max_length=64, default='', verbose_name='Получатель сообщения')
    creationDate = models.DateTimeField(default=timezone.now, editable=False)

    STATUS_CHOICES = (
        (1, 'Создано'),
        (2, 'Отправлено в telegram'),
        (3, 'Отправлено'),
        (4, 'Сбой отправки в telegram'),
        (5, 'Сбой отправки'),
        (6, 'В обработке'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )

    connectionId = models.CharField(max_length=32, default='', verbose_name="Параметр для подключения к другим моделям", help_text="Если нужно можно использовать для подключения к другим моделям, на пример: заказ, пользователь")
    messageType = models.CharField(max_length=32, default='', verbose_name="Тип сообщения", help_text="Используется если нужно, на пример тип: 'passwordRecovery', 'orderSended'")

    telegramResponse = models.TextField(blank=True, verbose_name= "Ответ сервера telegram при отправке")

    def __str__(self) -> str:
        return f"{self.receiver} -> {self.text} [status: {self.status}]"

class TelegramReceivedMessage(models.Model):
    text = models.TextField(verbose_name= "Текст сообщения")
    sender = models.CharField(max_length=64, default='', verbose_name='Отправитель сообщения')
    creationDate = models.DateTimeField(default=timezone.now, editable=False)

    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=72, default='', verbose_name='Имя отправителя сообщения')
    last_name = models.CharField(max_length=72, default='', verbose_name='Фамилия отправителя сообщения')
    username = models.CharField(max_length=72, default='', verbose_name='Имя пользователя отправителя сообщения')
    json = models.TextField(blank=False, verbose_name= "JSON сообщения")

    STATUS_CHOICES = (
        (1, 'Создано'),
        (2, 'Прочитано'),
        (3, 'Обработано'),
        (4, 'Отвечено'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )

    def __str__(self) -> str:
        return f"{self.username} -> {self.text} [status: {self.status}]"

class TelegramCallbackQuery(models.Model):

    data = models.TextField(verbose_name= "Данные коллбэка")
    sender = models.CharField(max_length=64, default='', verbose_name='Отправитель сообщения')
    creationDate = models.DateTimeField(default=timezone.now, editable=False)

    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=72, default='', verbose_name='Имя отправителя сообщения')
    last_name = models.CharField(max_length=72, default='', verbose_name='Фамилия отправителя сообщения')
    username = models.CharField(max_length=72, default='', verbose_name='Имя пользователя отправителя сообщения')

    json = models.TextField(blank=False, verbose_name= "JSON коллбэка")

    STATUS_CHOICES = (
        (1, 'Создано'),
        (2, 'Прочитано'),
        (3, 'Обработано'),
        (4, 'Отвечено'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )

    def __str__(self) -> str:
        return f"{self.username} -> {self.data} [status: {self.status}]"

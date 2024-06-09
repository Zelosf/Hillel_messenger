from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import MessageLog
from .models import Message


@receiver(post_save, sender=Message)
def log_message(sender, instance, created, **kwargs):
    action = 'Повідомлення надіслано' if created else 'Повідомлення відкориговано'
    author = instance.author
    MessageLog.objects.create(author=author, message=instance, action=action)
    #if any(user.is_superuser for user in instance.chat.participants.all()):
    #    messages.success(author, 'Вы успішно надіслали повідомлення суперюзеру')
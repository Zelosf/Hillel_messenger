from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import MessageLog, UserStatus, Message
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(post_save, sender=Message)
def log_message(sender, instance, created, **kwargs):
    action = 'Повідомлення надіслано' if created else 'Повідомлення відкориговано'
    author = instance.author
    MessageLog.objects.create(author=author, message=instance, action=action)


@receiver(user_logged_in)
def set_user_online(sender, user, request, **kwargs):
    user_status, created = UserStatus.objects.get_or_create(user=user)
    user_status.is_online = True
    user_status.save()

@receiver(user_logged_out)
def set_user_offline(sender, user, request, **kwargs):
    user_status, created = UserStatus.objects.get_or_create(user=user)
    user_status.is_online = False
    user_status.save()
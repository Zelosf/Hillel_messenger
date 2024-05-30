from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
	name = models.CharField(max_length=255)
	participants = models.ManyToManyField(User, related_name='chats')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		permissions = [
			("can_create_chat", "Can Create chat"),
			("can_add_users_to_chat", "Can Add users to chat"),
			("can_remove_users_from_chat", "Can Remove users from chat"),
		]

	def __str__(self):
		return self.name


class Message(models.Model):
	chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		permissions = [
			("can_edit_own_message", "Can Edit own message"),
			("can_delete_own_message", "Can Delete own message"),
		]
	def __str__(self):
		return f'{self.author.username}: {self.content[:20]}'

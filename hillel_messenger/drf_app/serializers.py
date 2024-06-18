from rest_framework import serializers
from messenger.models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = ['id', 'name', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ['id', 'chat', 'author', 'content', 'created_at', 'updated_at']
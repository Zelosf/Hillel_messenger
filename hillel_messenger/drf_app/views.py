from rest_framework import generics, permissions
from messenger.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class UserChats(generics.ListAPIView):
	serializer_class = ChatSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return self.request.user.chats.all()


class ChatMessages(generics.ListAPIView):
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		chat_id = self.kwargs['chat_id']
		user = self.request.user
		chat = Chat.objects.filter(id=chat_id, participants=user).first()
		return Message.objects.filter(chat=chat, author=user)


class MessageCreate(generics.CreateAPIView):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]


class MessageRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]

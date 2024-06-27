from django.urls import path
from .views import (
	UserChats,
	ChatMessages,
	MessageCreate,
	MessageRetrieveUpdateDelete
)

urlpatterns = [
	path('chats/', UserChats.as_view(), name = 'user-chats'),
	path('chat/<int:chat_id>/messages/', ChatMessages.as_view(), name = 'message_list_in_chat'),
	path('message/', MessageCreate.as_view(), name = 'message_create'),
	path('message/<int:pk>/', MessageRetrieveUpdateDelete.as_view(), name='message_RUD')
]
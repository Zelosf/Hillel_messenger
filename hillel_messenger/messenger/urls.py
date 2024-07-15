from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list.as_view(), name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail.as_view(), name='chat_detail'),
    path('chat/<int:chat_id>/send_message/', views.send_message.as_view(), name='send_message'),
    path('message/<int:message_id>/edit/', views.edit_message.as_view(), name='edit_message'),
    path('message/<int:message_id>/delete/', views.delete_message.as_view(), name='delete_message'),
    path('chat/<int:chat_id>/users/status/list/', views.user_status_list.as_view(), name='user_status_list'),
]
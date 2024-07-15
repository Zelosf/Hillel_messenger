from django.shortcuts import render, redirect
from .models import Chat, Message, UserStatus
from django.http import HttpResponseForbidden, Http404, JsonResponse
from django.contrib import messages
from django.views import View
from .mixins import (
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    UserIsParticipantMixin,
    JsonResponseMixin,
    FormValidMessageMixin,
    ObjectOwnerMixin
)

class chat_list(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(participants=request.user)
        return render(request, 'chats.html', {'chats': chats})

class chat_detail(CustomLoginRequiredMixin, UserIsParticipantMixin, View):
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id=chat_id)
        messages = chat.messages.all()
        return render(request, 'chat.html', {'chat': chat, 'chatmessages': messages})

class send_message(CustomLoginRequiredMixin, UserIsParticipantMixin, FormValidMessageMixin, View):
    success_message = "Message sent successfully."

    def post(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id=chat_id)
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, author=request.user, content=content)
            if chat.participants.count() == 2:
                other_user = chat.participants.exclude(id=request.user.id).first()
                if other_user.is_superuser:
                    messages.success(request, '!!!Ви успішно надіслали повідомлення суперюзеру!!!')
        return redirect('chat_detail', chat_id=chat.id)

class edit_message(CustomLoginRequiredMixin, CustomPermissionRequiredMixin, ObjectOwnerMixin, View):
    permission_required = 'messenger.can_edit_own_message'

    def get(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)
        return render(request, 'edit_message.html', {'message': message})

    def post(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)
        content = request.POST.get('content')
        if content:
            message.content = content
            message.save()
            return redirect('chat_detail', chat_id=message.chat.id)
        return render(request, 'edit_message.html', {'message': message})

class delete_message(CustomLoginRequiredMixin, CustomPermissionRequiredMixin, ObjectOwnerMixin, View):
    permission_required = 'messenger.can_delete_own_message'

    def post(self, request, message_id, *args, **kwargs):
        message = Message.objects.get(id=message_id)
        chat_id = message.chat.id
        message.delete()
        return redirect('chat_detail', chat_id=chat_id)

class user_status_list(CustomLoginRequiredMixin, UserIsParticipantMixin, JsonResponseMixin, View):
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id=chat_id)
        users_data = []
        for participant in chat.participants.all():
            try:
                user_status = UserStatus.objects.get(user=participant)
                users_data.append({'name': participant.username, 'is_online': user_status.is_online})
            except UserStatus.DoesNotExist:
                users_data.append({'name': participant.username, 'is_online': False})
        return self.render_to_json_response(users_data)

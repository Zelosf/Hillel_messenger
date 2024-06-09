from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Chat, Message, MessageLog
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages




@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chats.html', {'chats': chats})



@login_required
def chat_detail(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat not found")
    if request.user not in chat.participants.all():
        return HttpResponseForbidden()
    messages = chat.messages.all()
    return render(request, 'chat.html', {'chat': chat, 'chatmessages': messages})



@login_required
def send_message(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat not found")
    if request.user not in chat.participants.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, author=request.user, content=content)
            if chat.participants.count() == 2:
                other_user = chat.participants.exclude(id=request.user.id).first()
                if other_user.is_superuser:
                    messages.success(request, 'Ви успішно надіслали повідомлення суперюзеру')
    return redirect('chat_detail', chat_id=chat.id)



@login_required
@permission_required('messenger.can_edit_own_message')
def edit_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        raise Http404("Message not found")
    if request.user != message.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message.content = content
            message.save()
            return redirect('chat_detail', chat_id=message.chat.id)
    return render(request, 'edit_message.html', {'message': message})


@login_required
@permission_required('messenger.can_delete_own_message')
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        raise Http404("Message not found")
    if request.user != message.author:
        return HttpResponseForbidden()
    chat_id = message.chat.id
    message.delete()
    return redirect('chat_detail', chat_id=chat_id)

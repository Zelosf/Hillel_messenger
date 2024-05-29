from django.contrib import admin
from .models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	search_fields = ('name',)
	filter_horizontal = ('participants',)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'chat', 'content', 'updated_at')
	search_fields = ('author__username', 'content')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)

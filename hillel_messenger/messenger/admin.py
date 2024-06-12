from django.contrib import admin
from .models import Chat, Message, MessageLog, UserStatus


class ChatAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	search_fields = ('name',)
	filter_horizontal = ('participants',)


class MessageAdmin(admin.ModelAdmin):
	list_display = ('author', 'chat', 'content', 'updated_at')
	search_fields = ('author__username', 'content')


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'action', 'timestamp')


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserStatus)

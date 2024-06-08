from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('roomId', 'type', 'name')
    search_fields = ('roomId', 'name')
    list_filter = ('type',)
    filter_horizontal = ('member',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'message', 'timestamp')
    search_fields = ('message', 'user__username', 'chat__roomId')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
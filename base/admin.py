from django.contrib import admin
from .models import Room, Topic, Message, User

# Register your models here.

class UserList(admin.ModelAdmin):
    list_display = ('email', 'id')

admin.site.register(User, UserList)

class RoomList(admin.ModelAdmin):
    list_display = ('host', 'topic', 'name', 'description', 'updated', 'created', 'id')

admin.site.register(Room, RoomList)

class TopicList(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Topic, TopicList)

# coustom list display interface in http: // 127.0.0.1: 8000/admin/base/message/
class MessageList(admin.ModelAdmin):
    list_display = ('user', 'room', 'body', 'updated', 'created', )

admin.site.register(Message, MessageList)



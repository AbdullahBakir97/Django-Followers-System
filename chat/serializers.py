from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from accounts.models import User, OnlineUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ChatRoomSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True, read_only=True)
    members = serializers.ListField(write_only=True)

    def create(self, validated_data):
        member_objects = validated_data.pop('members')
        chat_room = ChatRoom.objects.create(**validated_data)
        chat_room.member.set(member_objects)
        return chat_room

    class Meta:
        model = ChatRoom
        exclude = ['id']

class ChatMessageSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userImage = serializers.ImageField(source='user.profile.image', read_only=True)

    class Meta:
        model = ChatMessage
        exclude = ['id', 'chat']

    def get_userName(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
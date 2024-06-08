from rest_framework import serializers
from .models import UserProfile, FollowRequest, Follower
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'is_private', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.save()

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return instance

class FollowRequestSerializer(serializers.ModelSerializer):


    class Meta:
        model = FollowRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at']

class FollowerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower', 'created_at']
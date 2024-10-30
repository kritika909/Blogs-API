from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'profileimg', 'bio', 'accentcolor', 'bgcolor']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following']

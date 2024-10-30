from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'cont', 'created_at']

    
from rest_framework import serializers
from .models import Post, Comment,Likes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at','like']
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value
    
    
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields='__all__'
        
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
        
    def validate(self, data):
        username=data.get('username')
        password=data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError("Please enter username and password")
        user=authenticate(username=username,password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
            
        return data
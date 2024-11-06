from .models import Post, Category
from rest_framework import serializers
from django.contrib.auth.models import User
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class SearchPostSerializer(serializers.Serializer):
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = '__all__'
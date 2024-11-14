from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
import redis
from utils.bloom_filter import BloomFilter
import logging
logger = logging.getLogger(__name__)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise ValidationError('Email or username already exists')

        # bloom_filter = BloomFilter(redis.from_url(settings.REDIS_CLIENT), 'user_registration_bloom', size=1000000, hash_count=3)
        # if bloom_filter.contains(email) or bloom_filter.contains(username):
        #     raise ValidationError('User with this email or username already exists.')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # bloom_filter = BloomFilter(settings.REDIS_CLIENT, 'user_registration_bloom', size=1000000, hash_count=3)
        # bloom_filter.add(user.email)
        # bloom_filter.add(user.username)

        return user
from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from rest_framework.views import APIView
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import Post
from .serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework import status

logger = logging.getLogger(__name__)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000
    def get_paginated_response(self, data):
        # Retrieve the current, next, and previous page numbers
        current_page = self.page.number
        next_page = self.page.next_page_number() if self.page.has_next() else None
        previous_page = self.page.previous_page_number() if self.page.has_previous() else None

        return Response({
            'total_count': self.page.paginator.count,
            'current_page': current_page,
            'next_page': next_page,
            'previous_page': previous_page,
            'data': data  # Rename 'results' to 'data'
        })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
    # Get the current page number from request query parameters
        page_number = request.query_params.get('page', 1)
        cache_key = f'post_list_page_{page_number}'

        # Try to get cached data for this page
        cached_data = cache.get(cache_key)

        if cached_data:
            # Return cached paginated response
            return Response(cached_data, status=status.HTTP_200_OK)
        
        # If data is not in cache, fetch from the database and paginate
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Ensure self.paginator.page is only accessed after paginate_queryset is called
            data = {
                'total_count': self.paginator.page.paginator.count,
                'current_page': self.paginator.page.number,
                'next_page': self.paginator.page.next_page_number() if self.paginator.page.has_next() else None,
                'previous_page': self.paginator.page.previous_page_number() if self.paginator.page.has_previous() else None,
                'data': serializer.data
            }
            # Cache the paginated response data
            cache.set(cache_key, data, timeout=60 * 15)  # Cache for 15 minutes
            return Response(data)

        # If no pagination is needed (e.g., single page), serialize and cache entire queryset
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'total_count': len(serializer.data),
            'current_page': 1,
            'next_page': None,
            'previous_page': None,
            'data': serializer.data
        }
        cache.set(cache_key, data, timeout=60 * 15)
        return Response(data)


    def create(self, request, *args, **kwargs):
    # Serialize the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Clear relevant cache (if you cache individual pages, you might want to loop through them and delete each one)
        self.clear_cache()
        
        # Respond with the newly created post
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.clear_cache()  # Clear cache after update
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.clear_cache()  # Clear cache after deletion
        return response
    

    def clear_cache(self):
    # Calculate total number of pages based on queryset and page size
        total_items = self.get_queryset().count()
        page_size = self.paginator.page_size
        num_pages = (total_items // page_size) + (1 if total_items % page_size > 0 else 0)

        # Clear all cached pages for the post list
        for page in range(1, num_pages + 1):
            cache.delete(f'post_list_page_{page}')


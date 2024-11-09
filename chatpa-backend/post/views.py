import abc
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import Post
from .serializers import PostSerializer, SearchPostSerializer
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from post.documents import  PostDocument, UserDocument, CategoryDocument
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination


logger = logging.getLogger(__name__)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    def get_paginated_response(self, data):
        # Retrieve the current, next, and previous page numbers
        current_page = self.page.number
        next_page = self.page.next_page_number() if self.page.has_next() else None
        previous_page = self.page.previous_page_number() if self.page.has_previous() else None

        return Response({
            'current_page': current_page,
            'next_page': next_page,
            'previous_page': previous_page,
            'page_size': self.page_size,
            'data': data  # Rename 'results' to 'data'
        })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        # Get page number and search query from request
        page_number = request.query_params.get('page', 1)
        search_query = request.query_params.get('search_query', '').strip()

        # Check if there's a search query; if so, skip caching
        if not search_query:
            cache_key = f'post_list_page_{page_number}'
            logger.info(f"Cache key: {cache_key}")

            # Check for cached data only if no search query is present
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info("Returning cached data")
                return Response(cached_data, status=status.HTTP_200_OK)
        
        # Fetch data from the database and apply pagination
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
            
            # Only cache if no search query is present
            if not search_query:
                cache.set(cache_key, data, timeout=60 * 15)
            return Response(data)

        # For unpaginated data (single page)
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'total_count': len(serializer.data),
            'current_page': 1,
            'next_page': None,
            'previous_page': None,
            'data': serializer.data
        }
        if not search_query:
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
    

    def get_queryset(self):
        search_query = self.request.query_params.get('search_query', '').strip()
        logger.info(f"Search query: {search_query}")
        
        if search_query:
            vector = (
                SearchVector('title', weight='A') +
                SearchVector('content', weight='B') +
                SearchVector('category__name', weight='C')
            )
            query = SearchQuery(search_query)
            queryset = Post.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
        else:
            queryset = super().get_queryset()

        return queryset

    def clear_cache(self):
    # Calculate total number of pages based on queryset and page size
        total_items = self.get_queryset().count()
        page_size = self.paginator.page_size
        num_pages = (total_items // page_size) + (1 if total_items % page_size > 0 else 0)

        # Clear all cached pages for the post list
        for page in range(1, num_pages + 1):
            cache.delete(f'post_list_page_{page}')



class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        print("query", query)
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            logger.info(f"Results: {results}")
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(e, status=500)

class SearchPost(PaginatedElasticSearchAPIView):
    document_class = PostDocument
    serializer_class = SearchPostSerializer

    def generate_q_expression(self, query):
        return Q(
                "multi_match", query=query,
                fields=[
                    "title",
                ])
        
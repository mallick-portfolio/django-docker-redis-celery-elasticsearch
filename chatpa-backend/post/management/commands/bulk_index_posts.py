# my_app/management/commands/bulk_index_posts.py

from django.core.management.base import BaseCommand
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from post.models import Post
from post.documents import PostDocument

class Command(BaseCommand):
    help = "Bulk index all Post data to Elasticsearch"

    def handle(self, *args, **kwargs):
        es = Elasticsearch(hosts=["http://elasticsearch:9200"])
        index_name = PostDocument.Index.name

        # Optimize settings for faster indexing
        es.indices.put_settings(index=index_name, body={"index": {"refresh_interval": "-1"}})
        es.indices.put_settings(index=index_name, body={"index": {"number_of_replicas": 0}})

        # Define bulk indexing function
        def bulk_index_posts(batch_size=1000):
            posts = Post.objects.all().iterator()
            actions = []

            for count, post in enumerate(posts, start=1):
                actions.append({
                    "_op_type": "index",
                    "_index": index_name,
                    "_id": post.id,
                    "_source": {
                        "title": post.title,
                        "content": post.content,
                        "created_at": post.created_at,
                        "updated_at": post.updated_at,
                        "author": {
                            "username": post.author.username,
                            "email": post.author.email,
                            "first_name": post.author.first_name,
                            "last_name": post.author.last_name,
                        },
                        "category": {
                            "name": post.category.name,
                            "description": post.category.description,
                        },
                    },
                })

                if count % batch_size == 0:
                    bulk(es, actions)
                    actions = []  # Clear actions for next batch

            if actions:
                bulk(es, actions)  # Index remaining posts

        # Run bulk indexing
        bulk_index_posts(batch_size=1000)

        # Restore settings after indexing
        es.indices.put_settings(index=index_name, body={"index": {"refresh_interval": "1s"}})
        es.indices.put_settings(index=index_name, body={"index": {"number_of_replicas": 1}})

        self.stdout.write(self.style.SUCCESS("Successfully indexed all posts."))

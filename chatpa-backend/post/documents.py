from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, Category
from django.contrib.auth.models import User


@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Category
        fields = [
            'name',
            'description',
        ]


@registry.register_document
class PostDocument(Document):
    author = fields.ObjectField(properties={
        'username': fields.TextField(),
        'email': fields.TextField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
    })

    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'description': fields.TextField(),
    })
    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Post
        fields = [
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

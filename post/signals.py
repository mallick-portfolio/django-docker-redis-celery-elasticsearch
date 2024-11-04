# your_app/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post
from .elasticsearch import PostDocument

@receiver(post_save, sender=Post)
def update_post_in_index(sender, instance, **kwargs):
    # Update or create the document in Elasticsearch
    PostDocument().update(instance)

@receiver(post_delete, sender=Post)
def delete_post_from_index(sender, instance, **kwargs):
    # Delete the document from Elasticsearch
    PostDocument().delete(instance)

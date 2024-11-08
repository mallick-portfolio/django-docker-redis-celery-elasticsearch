import random
import string
import logging
from django.core.management.base import BaseCommand
from post.models import Post, Category
from django.utils.text import slugify
from django.contrib.auth.models import User
from faker import Faker

faker = Faker()

# Configure logger for this command
logger = logging.getLogger('post_generation')

class Command(BaseCommand):
    help = 'Generate 10,000,00 random posts and assign random categories'

    def add_arguments(self, parser):
        # Optionally, you can pass the number of posts to create as an argument
        parser.add_argument(
            '--posts',
            type=int,
            default=1000000,
            help='Number of random posts to generate'
        )

    def handle(self, *args, **kwargs):
        num_posts = kwargs['posts']
        batch_size = 1000  # You can adjust this depending on memory limits

        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return

        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please create categories first.'))
            return

        def generate_random_string(length=10):
            """Generate a random string of fixed length."""
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

        def generate_random_post_title():
            """Generate a random, unique title for the post."""
            while True:
                # Generate a random title with 3-6 words
                title = ' '.join(faker.words(nb=random.randint(3, 6))).capitalize()
                # Check if the title already exists in the Post model
                if not Post.objects.filter(slug=slugify(title)).exists():
                    return title
        
        posts_to_create = []
        for i in range(num_posts):
            title = generate_random_post_title()
            category = random.choice(categories)
            content = generate_random_string(500)  # Assuming 500 characters for content
            slug = slugify(title)
            author = random.choice(users)

            post = Post(
                title=title,
                content=content,
                slug=slug,
                category=category,
                author=author
            )
            posts_to_create.append(post)

            # Insert posts in batches
            if len(posts_to_create) >= batch_size:
                Post.objects.bulk_create(posts_to_create)
                posts_to_create.clear()  # Clear the list after bulk insert
                logger.info(f'Inserted {i + 1} posts')

        # Insert remaining posts
        if posts_to_create:
            Post.objects.bulk_create(posts_to_create)
            logger.info(f'Inserted the last batch of posts, total: {num_posts}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_posts} posts!'))


import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User  # Or your custom user model
from faker import Faker
import logging

# Configure logger for this command
logger = logging.getLogger('user_generation')

class Command(BaseCommand):
    help = 'Generate random users with random names'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=100000,
            help='Number of random users to generate'
        )

    def handle(self, *args, **kwargs):
        num_users = kwargs['users']
        batch_size = 1000  # Adjust this based on your memory and database speed
        faker = Faker()

        users_to_create = []
        for i in range(num_users):
            first_name = faker.first_name()
            last_name = faker.last_name()
            username = faker.user_name()
            email = faker.email()

            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password('password123')  # Set a default password for all users
            users_to_create.append(user)

            # Insert users in batches
            if len(users_to_create) >= batch_size:
                User.objects.bulk_create(users_to_create)
                users_to_create.clear()  # Clear the list after bulk insert
                logger.info(f'Inserted {i + 1} users')

        # Insert remaining users
        if users_to_create:
            User.objects.bulk_create(users_to_create)
            logger.info(f'Inserted the last batch of users, total: {num_users}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_users} users!'))

# Chatpa Project

This project is a Docker-based backend API for managing posts, categories, and users. It integrates PostgreSQL for data storage, Redis for caching, and Elasticsearch for real-time search capabilities.

## Prerequisites

- Docker (Make sure Docker is installed and running)

## Getting Started

Follow these steps to set up and run the project.

```bash
# Clone the repository
git clone https://github.com/mallick-portfolio/django-docker-redis-celery-elasticsearch.git
cd <project_directory>

# Inside the chatpa-backend directory, copy the environment files and set values
cd chatpa-backend
cp db.env.example db.env
cp backend.env.example backend.env

# Edit db.env and backend.env to set the required environment variable values

# Go back to the root project directory and start Docker containers
cd ..
docker compose up

# Get the backend container name
docker ps  # This will list running containers; look for the backend container's name

# Run migrations and seed initial data (replace <backend_container_name> with the backend container name)
docker exec -it <backend_container_name> python manage.py migrate
docker exec -it <backend_container_name> python manage.py add_users
docker exec -it <backend_container_name> python manage.py add_categories

# Generate 1 million sample posts (this will take a few minutes)
docker exec -it <backend_container_name> python manage.py add_posts

# Rebuild the Elasticsearch index
docker exec -it <backend_container_name> python manage.py search_index --rebuild

```

## Full-Text Search with PostgreSQL (replace <post_title> with your search term)

http://localhost:8000/api/v1/posts/?search_query=<post_title>

## Paginated and Cached Post Retrieval (using Redis, replace <page_number> with the desired page number)

http://localhost:8000/api/v1/posts/?page=<page_number>

## Test Elasticsearch Search (visit in browser and type a post title in the search bar)

http://localhost:3000/

#### Let me know if there’s anything more you’d like added or clarified.

#### Feel free to give me feedback on the code quality and documentation.

from django.core.management.base import BaseCommand
from post.models import Category
import logging

logger = logging.getLogger('category_creationg')

class Command(BaseCommand):
    help = 'Create multiple categories'

    def handle(self, *args, **kwargs):
        categories = [
                {"name": "Technology", "description": "All about the latest in tech, gadgets, and innovation."},
                {"name": "Science", "description": "Discoveries, research, and developments in various scientific fields."},
                {"name": "Health & Wellness", "description": "Tips and advice on physical and mental health."},
                {"name": "Fitness", "description": "Guides, routines, and tips for staying fit and healthy."},
                {"name": "Food & Recipes", "description": "Delicious recipes, cooking tips, and food trends."},
                {"name": "Travel", "description": "Exploring destinations, travel tips, and adventure stories."},
                {"name": "Finance", "description": "Personal finance, investments, and money management tips."},
                {"name": "Business", "description": "Latest trends, strategies, and advice for businesses and entrepreneurs."},
                {"name": "Education", "description": "Learning resources, tools, and education news."},
                {"name": "Environment", "description": "Climate change, sustainability, and environmental news."},
                {"name": "Fashion", "description": "Latest trends and tips in fashion and style."},
                {"name": "Beauty", "description": "Makeup, skincare, and beauty routines."},
                {"name": "Parenting", "description": "Advice and tips on raising children."},
                {"name": "Pets", "description": "Care, tips, and news for pet owners."},
                {"name": "Automotive", "description": "Cars, reviews, and tips for auto enthusiasts."},
                {"name": "Real Estate", "description": "Home buying, selling, and real estate market trends."},
                {"name": "Sports", "description": "News and updates on popular sports and events."},
                {"name": "Entertainment", "description": "Movies, TV shows, and celebrity news."},
                {"name": "Music", "description": "Reviews and news in the world of music."},
                {"name": "Gaming", "description": "Latest in video games, reviews, and gaming culture."},
                {"name": "Art & Design", "description": "Exploring creativity in the world of art and design."},
                {"name": "Photography", "description": "Tips and inspiration for photographers."},
                {"name": "DIY & Crafts", "description": "Creative projects, DIY tips, and crafting ideas."},
                {"name": "Home Improvement", "description": "Renovation tips and home decor advice."},
                {"name": "Gardening", "description": "Tips and tricks for growing plants and maintaining gardens."},
                {"name": "Relationships", "description": "Advice on relationships, dating, and love."},
                {"name": "Spirituality", "description": "Exploring personal growth, mindfulness, and spirituality."},
                {"name": "Career & Job Search", "description": "Guides and tips for advancing your career."},
                {"name": "Marketing", "description": "Strategies, trends, and tips for marketing professionals."},
                {"name": "Productivity", "description": "Advice on staying productive and organized."},
                {"name": "Self-Development", "description": "Tips for personal growth and improving your skills."},
                {"name": "History", "description": "Exploring important events and figures in history."},
                {"name": "Politics", "description": "News and insights on political events and policies."},
                {"name": "Legal", "description": "Legal advice, news, and updates in the field of law."},
                {"name": "Economics", "description": "Understanding economic trends and financial policies."},
                {"name": "Technology Reviews", "description": "In-depth reviews of the latest gadgets and software."},
                {"name": "Social Media", "description": "Trends, tips, and best practices for social media platforms."},
                {"name": "Programming", "description": "Guides, tutorials, and updates in the world of coding."},
                {"name": "Cybersecurity", "description": "Protecting your data and devices from digital threats."},
                {"name": "Artificial Intelligence", "description": "Exploring developments in AI and machine learning."},
                {"name": "Blockchain & Cryptocurrency", "description": "Understanding blockchain technology and crypto markets."},
                {"name": "Virtual Reality", "description": "News and trends in the world of VR and immersive tech."},
                {"name": "E-commerce", "description": "Trends, strategies, and tips for online retail."},
                {"name": "Sustainability", "description": "Ideas and practices for sustainable living."},
                {"name": "Psychology", "description": "Exploring human behavior and the mind."},
                {"name": "Philosophy", "description": "Debates, questions, and insights into philosophy."},
                {"name": "Astronomy", "description": "News and discoveries about space and the universe."},
                {"name": "Cooking Tips", "description": "Practical advice for home cooks and food lovers."},
                {"name": "Luxury", "description": "High-end products, services, and lifestyles."},
                {"name": "Life Hacks", "description": "Simple tricks and tips to make daily life easier."}
            ]

        for category in categories:
            Category.objects.create(name=category["name"], description=category["description"])
            logger.info(f'Category "{category["name"]}" created or already exists.')

        logger.info("Categories created successfully!")
        self.stdout.write(self.style.SUCCESS(f"{len(categories)} categories created successfully!"))

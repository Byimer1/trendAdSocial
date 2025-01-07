from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files import File
from posts.models import Post, Comment
from ads.models import Ad
from notifications.models import Notification
from direct_messages.models import Message, Conversation
import random
from datetime import timedelta
import os
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates mock data for testing'

    def __init__(self):
        super().__init__()
        self.users_data = [
            {
                'username': 'emma_wilson',
                'email': 'emma.wilson@example.com',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'bio': 'Travel enthusiast | Coffee lover | Professional photographer',
                'gender': 'F',
                'profile_pic': 'female1.jpg'
            },
            {
                'username': 'alex_parker',
                'email': 'alex.parker@example.com',
                'first_name': 'Alex',
                'last_name': 'Parker',
                'bio': 'Tech geek | Fitness freak | Always learning',
                'gender': 'M',
                'profile_pic': 'male1.jpg'
            },
            {
                'username': 'sophia_chen',
                'email': 'sophia.chen@example.com',
                'first_name': 'Sophia',
                'last_name': 'Chen',
                'bio': 'Food blogger | Recipe developer | Living life deliciously',
                'gender': 'F',
                'profile_pic': 'female2.jpg'
            },
            {
                'username': 'james_smith',
                'email': 'james.smith@example.com',
                'first_name': 'James',
                'last_name': 'Smith',
                'bio': 'Sports fanatic | Guitar player | Adventure seeker',
                'gender': 'M',
                'profile_pic': 'male2.jpg'
            },
            {
                'username': 'olivia_brown',
                'email': 'olivia.brown@example.com',
                'first_name': 'Olivia',
                'last_name': 'Brown',
                'bio': 'Artist | Nature lover | Spreading positivity',
                'gender': 'F',
                'profile_pic': 'female3.jpg'
            },
            {
                'username': 'michael_davis',
                'email': 'michael.davis@example.com',
                'first_name': 'Michael',
                'last_name': 'Davis',
                'bio': 'Software engineer | Gamer | Dog person',
                'gender': 'M',
                'profile_pic': 'male3.jpg'
            },
            {
                'username': 'isabella_garcia',
                'email': 'isabella.garcia@example.com',
                'first_name': 'Isabella',
                'last_name': 'Garcia',
                'bio': 'Fashion designer | Travel addict | Living my best life',
                'gender': 'F',
                'profile_pic': 'female4.jpg'
            },
            {
                'username': 'william_taylor',
                'email': 'william.taylor@example.com',
                'first_name': 'William',
                'last_name': 'Taylor',
                'bio': 'Musician | Coffee addict | Always exploring',
                'gender': 'M',
                'profile_pic': 'male4.jpg'
            },
            {
                'username': 'ava_martinez',
                'email': 'ava.martinez@example.com',
                'first_name': 'Ava',
                'last_name': 'Martinez',
                'bio': 'Yoga instructor | Mindfulness coach | Plant mom',
                'gender': 'F',
                'profile_pic': 'female5.jpg'
            },
            {
                'username': 'daniel_lee',
                'email': 'daniel.lee@example.com',
                'first_name': 'Daniel',
                'last_name': 'Lee',
                'bio': 'Chef | Food photographer | World traveler',
                'gender': 'M',
                'profile_pic': 'male5.jpg'
            }
        ]

        self.post_captions = [
            "Living my best life! 🌟",
            "Perfect day for an adventure 🌄",
            "Coffee and good vibes ☕️",
            "Weekend mood 🎉",
            "Nature therapy 🌿",
            "City lights and good times 🌃",
            "Beach day with friends 🏖",
            "Cooking up something special 🍳",
            "Fitness journey continues 💪",
            "Travel memories ✈️"
        ]

        self.locations = [
            "New York, USA",
            "Paris, France",
            "Tokyo, Japan",
            "London, UK",
            "Sydney, Australia",
            "Dubai, UAE",
            "Rome, Italy",
            "Barcelona, Spain",
            "Amsterdam, Netherlands",
            "Singapore"
        ]

        self.comments = [
            "This is amazing! 😍",
            "Love this photo!",
            "Perfect shot 📸",
            "Goals! 🙌",
            "Beautiful place!",
            "Miss you! ❤️",
            "Can't wait to visit!",
            "Looking good!",
            "Great vibes ✨",
            "Awesome photo!"
        ]

        self.ad_titles = [
            "Latest iPhone - Great Deal!",
            "Stylish Summer Collection",
            "Luxury Apartment for Rent",
            "Gaming Laptop - Special Offer",
            "Handmade Jewelry Sale",
            "Organic Food Delivery",
            "Fitness Equipment",
            "Designer Watches",
            "Home Decor Items",
            "Professional Camera Kit"
        ]

        self.ad_descriptions = [
            "Brand new iPhone with all accessories. Limited time offer!",
            "New summer collection with amazing designs. All sizes available.",
            "Spacious 2-bedroom apartment in prime location. Modern amenities.",
            "High-performance gaming laptop with RTX 3080. Perfect for gamers!",
            "Unique handmade jewelry pieces. Perfect for special occasions.",
            "Fresh organic produce delivered to your doorstep weekly.",
            "Premium quality fitness equipment for home workouts.",
            "Authentic designer watches at discounted prices.",
            "Beautiful home decor items to enhance your living space.",
            "Professional camera kit with multiple lenses and accessories."
        ]

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating mock data...')
        
        # Ensure media directories exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'avatars'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'posts'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'ads'), exist_ok=True)
        
        # Create users
        created_users = self.create_users()
        
        # Create posts and comments
        self.create_posts(created_users)
        
        # Create follows
        self.create_follows(created_users)
        
        # Create ads
        self.create_ads(created_users)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated mock data!'))

    def create_users(self):
        created_users = []
        for user_data in self.users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='testpass123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.bio = user_data['bio']
            
            # Set avatar when provided
            avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', user_data['profile_pic'])
            if os.path.exists(avatar_path):
                with open(avatar_path, 'rb') as f:
                    user.avatar.save(user_data['profile_pic'], File(f), save=True)
            
            user.save()
            created_users.append(user)
            self.stdout.write(f'Created user: {user.username}')
        return created_users

    def create_posts(self, users):
        for i in range(30):  # 30 posts
            user = random.choice(users)
            post = Post.objects.create(
                user=user,
                caption=random.choice(self.post_captions),
                location=random.choice(self.locations)
            )
            
            # Set post image when provided
            post_image_path = os.path.join(settings.MEDIA_ROOT, 'posts', f'post{i+1}.jpg')
            if os.path.exists(post_image_path):
                with open(post_image_path, 'rb') as f:
                    post.image.save(f'post{i+1}.jpg', File(f), save=True)
            
            # Add likes
            for _ in range(random.randint(5, 15)):
                liker = random.choice(users)
                post.likes.add(liker)
            
            # Add comments
            for _ in range(random.randint(3, 8)):
                commenter = random.choice(users)
                Comment.objects.create(
                    user=commenter,
                    post=post,
                    text=random.choice(self.comments)
                )
            
            self.stdout.write(f'Created post {i+1} with likes and comments')

    def create_follows(self, users):
        for user in users:
            # Each user follows 5-7 random users
            to_follow = random.sample([u for u in users if u != user], random.randint(5, 7))
            for follow_user in to_follow:
                user.following.add(follow_user)
            self.stdout.write(f'Created follows for: {user.username}')

    def create_ads(self, users):
        for i in range(10):  # 10 ads
            user = random.choice(users)
            ad = Ad.objects.create(
                user=user,
                title=self.ad_titles[i],
                description=self.ad_descriptions[i],
                price=random.uniform(50, 1000),
                location=random.choice(self.locations),
                is_sponsored=random.choice([True, False])
            )
            
            # Set ad image when provided
            ad_image_path = os.path.join(settings.MEDIA_ROOT, 'ads', f'ad{i+1}.jpg')
            if os.path.exists(ad_image_path):
                with open(ad_image_path, 'rb') as f:
                    ad.image.save(f'ad{i+1}.jpg', File(f), save=True)
            
            self.stdout.write(f'Created ad: {ad.title}') 
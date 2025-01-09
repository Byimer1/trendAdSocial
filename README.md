# Biruk's SocialHub: Redefining Connection and Content Sharing

A dynamic social media web application inspired by Instagram, designed for seamless user interaction and content sharing built with Django, featuring a clean and modern UI using Django templates and Bootstrap 5.

## Features

### User Management
- Custom user model with profile pictures
- User authentication (login, register, password reset)
- Profile management (edit profile, change password)
- Follow/Unfollow system
- User search functionality

### Posts
- Create, edit, and delete posts
- Upload images with captions
- Like/Unlike posts
- Comment on posts
- Save posts for later
- Explore page for discovering new contents
- Infinite scroll for better UX

### Direct Messages
- Private conversations between users
- Real-time messaging
- Read receipts
- Message notifications

### Notifications
- Notification system for:
  - Likes
  - Comments
  - Follows
  - Direct messages
- Mark notifications as read

## Technical Architecture

### Database Schema

#### Users App
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/')
    website = models.URLField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Posts App
```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    saved_by = models.ManyToManyField(User, related_name='saved_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Direct Messages App
```python
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Notifications App
```python
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message')
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Project Structure
```
bukisha/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
│   ├── avatars/
│   └── posts/
├── templates/
│   ├── base/
│   ├── users/
│   ├── posts/
│   ├── direct_messages/
│   └── notifications/
├── socialhub/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
├── posts/
├── direct_messages/
└── notifications/
```

## Development Workflow

1. **Setup Development Environment**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/bukisha.git
   cd bukisha

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Create .env file
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Implementation Steps

1. **Project Setup**
   - Create Django project and apps
   - Configure settings.py
   - Set up static and media files
   - Create base templates

2. **User Authentication**
   - Implement custom user model
   - Create authentication views (login, register, etc.)
   - Design authentication templates
   - Add email verification

3. **User Profiles**
   - Create profile views
   - Implement follow system
   - Add profile editing
   - Create profile templates

4. **Posts**
   - Implement post model and views
   - Create post creation form
   - Add like functionality
   - Implement comments
   - Create post templates

5. **Direct Messages**
   - Create messaging system
   - Implement real-time updates
   - Design conversation UI
   - Add message notifications

6. **Notifications**
   - Create notification system
   - Implement real-time notifications
   - Add notification templates

7. **Feed and Explore**
   - Create home feed
   - Implement explore page
   - Add infinite scroll
   - Optimize queries

## Dependencies

```python
Django==4.2.8
django-cleanup==8.0.0
django-crispy-forms==2.1
crispy-bootstrap5==2023.10
Pillow==10.1.0
python-dotenv==1.0.0
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## Push Notifications Setup

### Firebase Configuration
1. Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/)
2. Generate a new private key for your service account:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `firebase-service-account.json` in the project root directory
3. Add the following to your `.env` file:
   ```
   FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
   ```

### Device Token Management
The application supports push notifications through Firebase Cloud Messaging (FCM). To register a device:

1. Register a device token:
   ```http
   POST /api/users/register_device/
   {
     "token": "your-fcm-token",
     "device_type": "android|ios|web"
   }
   ```

2. Unregister a device token:
   ```http
   POST /api/users/unregister_device/
   {
     "token": "your-fcm-token"
   }
   ```

Push notifications are automatically sent for:
- New followers
- New likes on posts
- New comments on posts
- Direct messages 

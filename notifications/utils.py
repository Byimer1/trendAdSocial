from .models import Notification

def create_notification(recipient, sender, notification_type, text, post=None):
    """
    Create a notification for a user.
    
    Args:
        recipient: User object - The user who will receive the notification
        sender: User object - The user who triggered the notification
        notification_type: str - Type of notification ('like', 'comment', 'follow', 'message')
        text: str - The notification message
        post: Post object (optional) - Related post if applicable
    """
    if recipient != sender:  # Don't create notifications for own actions
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            text=text,
            post=post
        )

def create_like_notification(post, user):
    """Create a notification when a user likes a post."""
    create_notification(
        recipient=post.user,
        sender=user,
        notification_type='like',
        text='liked your post.',
        post=post
    )

def create_comment_notification(post, user, comment_text):
    """Create a notification when a user comments on a post."""
    create_notification(
        recipient=post.user,
        sender=user,
        notification_type='comment',
        text=f'commented: {comment_text[:50]}...' if len(comment_text) > 50 else f'commented: {comment_text}',
        post=post
    )

def create_follow_notification(followed_user, follower):
    """Create a notification when a user follows another user."""
    create_notification(
        recipient=followed_user,
        sender=follower,
        notification_type='follow',
        text='started following you.'
    )

def create_message_notification(conversation, sender, message_content):
    """Create a notification when a user receives a message."""
    recipient = conversation.other_participant(sender)
    create_notification(
        recipient=recipient,
        sender=sender,
        notification_type='message',
        text=f'sent you a message: {message_content[:50]}...' if len(message_content) > 50 else f'sent you a message: {message_content}'
    ) 
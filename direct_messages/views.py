from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Max, Count, OuterRef, Subquery
from .models import Conversation, Message
from users.models import User

@login_required
def inbox_view(request):
    last_message_subquery = Message.objects.filter(
        conversation=OuterRef('pk')
    ).order_by('-created_at').values('content')[:1]

    conversations = request.user.conversations.annotate(
        unread_count=Count(
            'messages',
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user)
        ),
        last_message_time=Max('messages__created_at'),
        last_message_content=Subquery(last_message_subquery)
    ).order_by('-last_message_time')
    
    return render(request, 'direct_messages/inbox.html', {
        'conversations': conversations
    })

@login_required
def new_conversation(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            other_user = User.objects.get(username=username)
            
            # Check if conversation already exists
            conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=other_user
            ).first()
            
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, other_user)
            
            return redirect('direct_messages:conversation_detail', conversation_id=conversation.id)
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return render(request, 'direct_messages/new_conversation.html')

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('messages__sender'),
        id=conversation_id,
        participants=request.user
    )
    
    # Mark messages as read
    conversation.messages.filter(
        ~Q(sender=request.user),
        is_read=False
    ).update(is_read=True)
    
    return render(request, 'direct_messages/conversation_detail.html', {
        'conversation': conversation,
        'other_user': conversation.other_participant(request.user)
    })

@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )
        
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'id': message.id,
                        'content': message.content,
                        'created_at': message.created_at.strftime('%I:%M %p'),
                        'is_sender': True
                    }
                })
    
    return redirect('direct_messages:conversation_detail', conversation_id=conversation_id)

@login_required
def mark_messages_read(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )
        
        conversation.messages.filter(
            ~Q(sender=request.user),
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def unread_count(request):
    count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(
        sender=request.user
    ).count()
    
    return JsonResponse({'count': count})

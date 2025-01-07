from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic import DetailView
from django.core.paginator import Paginator
from .models import User
from .forms import UserRegisterForm, UserUpdateForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get paginated posts
        posts = user.posts.all().order_by('-created_at')
        paginator = Paginator(posts, 12)  # Show 12 posts per page
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        
        context['posts'] = posts
        context['is_following'] = (
            self.request.user.is_authenticated and
            user in self.request.user.following.all()
        )
        return context

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/settings.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def follow_view(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user == user_to_follow:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('profile', username=user_to_follow.username)
    
    if request.method == 'POST':
        if user_to_follow in request.user.following.all():
            request.user.following.remove(user_to_follow)
            messages.success(request, f'You have unfollowed {user_to_follow.username}.')
        else:
            request.user.following.add(user_to_follow)
            messages.success(request, f'You are now following {user_to_follow.username}.')
    
    return redirect('profile', username=user_to_follow.username)

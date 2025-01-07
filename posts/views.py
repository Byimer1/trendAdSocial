from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        # Get posts from users the current user is following and their own posts
        following = self.request.user.following.all()
        return Post.objects.filter(
            Q(user__in=following) | Q(user=self.request.user)
        ).select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/explore.html'
    context_object_name = 'posts'
    paginate_by = 15
    
    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user).select_related('user').order_by('-created_at')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('user').order_by('created_at')
        return context

class SavedPostsView(LoginRequiredMixin, ListView):
    template_name = 'posts/saved_posts.html'
    context_object_name = 'posts'
    paginate_by = 15
    
    def get_queryset(self):
        return self.request.user.saved_posts.select_related('user').order_by('-created_at')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted.')
        return redirect('users:profile', username=request.user.username)
    
    return redirect('posts:post_detail', pk=pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    return redirect('posts:post_detail', pk=pk)

@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        if post.saved_by.filter(id=request.user.id).exists():
            post.saved_by.remove(request.user)
            saved = False
        else:
            post.saved_by.add(request.user)
            saved = True
        
        return JsonResponse({
            'saved': saved
        })
    
    return redirect('posts:post_detail', pk=pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'username': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%B %d, %Y %I:%M %p')
            })
    
    return redirect('posts:post_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    post_pk = comment.post.pk
    
    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'status': 'success'})
    
    return redirect('posts:post_detail', pk=post_pk)

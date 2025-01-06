from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import render, redirect
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm
from .models import LikeDislike
from django.http import HttpResponse


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    featured_posts = Post.objects.filter(is_featured=True)
    return render(request, 'blog/home.html', {'posts': posts, 'featured_posts': featured_posts})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    like_count = post.like_dislike.filter(is_like=True).count()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                # Optionally, redirect to the same page to prevent form resubmission
                return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')  # Redirect to login page or handle as needed
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'like_count': like_count})
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new post to the database
            return redirect('home')  # Redirect to the home page after successful submission
    else:
        form = PostForm()  # Display an empty form for GET request

    return render(request, 'blog/add_post.html', {'form': form})

def home(request):
    posts_list = Post.objects.all().order_by('-created_at')  # Retrieve all posts, ordered by newest first
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    posts = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'blog/home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    query = request.GET.get('q', '')  # Default to empty string if no query is present
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.all()

    featured_posts = Post.objects.filter(is_featured=True)  # Example for featured posts

    context = {
        'posts': posts,
        'featured_posts': featured_posts,
    }

    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'posts': page_obj})

def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'blog/profile.html', {'form': form})


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        existing_like = LikeDislike.objects.filter(post=post, user=request.user).first()
        if existing_like:
            existing_like.is_like = not existing_like.is_like
            existing_like.save()
        else:
            LikeDislike.objects.create(post=post, user=request.user, is_like=True)
    else:
        messages.error(request, "You must be logged in to like a post.")
        return redirect('login')  # Redirect to login page or handle as needed

    return redirect('post_detail', post_id=post.id)
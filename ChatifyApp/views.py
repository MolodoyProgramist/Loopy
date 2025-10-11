from django.shortcuts import get_object_or_404, redirect, render
from .models import Groups, Post, FriendRequest, Message, Notification, Rating,Chat, Comment, User
from .forms import CommentForm, PostForm, UserFrom


def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = user.posts.all()
    return render(request, 'profile.html', {'user': user, 'posts': posts})


def add_post(request):
    if request.method == 'POST':  # если пользователь отправляет форму
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile', user_id=request.user.id)
    else:  # если просто открывает страницу
        form = PostForm()
    return render(request, 'Posts/add_post.html', {'form': form})


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('Posts/post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'Posts/add_comment.html', {'form': form, 'post': post})


def main_view(request):
    # Берем все посты текущего пользователя
    posts = Post.objects.all()

    # Передаем их в шаблон
    return render(request, "main.html", {
        "posts": posts
    })
    
def search_view(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(content__icontains=query)
    users = User.objects.filter(username__icontains=query)
    groups = Groups.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'posts': posts,
        'users': users,
        'groups': groups,
    }
    return render(request, 'search_results.html', context)

# Create your views here.

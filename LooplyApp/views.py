from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PostForm, UserFrom
from .models import User, Groups, Post, FriendRequest, Message, Notification, Rating,Chat, Comment, Follow
from django.contrib.auth.decorators import login_required
from auth_system.views import logout


def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=profile_user)

    # Проверяем, подписан ли текущий пользователь
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'account/profile.html', context)

def profile_userView(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=profile_user)

    # Проверяем, подписан ли текущий пользователь
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'account/profile_user.html', context)


@login_required
def follow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if target != request.user:
        Follow.objects.get_or_create(follower=request.user, following=target)

    return redirect('profile_user', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    Follow.objects.filter(follower=request.user, following=target).delete()

    return redirect('profile_user', user_id=user_id)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        avatar = request.FILES.get("avatar")

        # обновляем данные
        user.username = username
        user.email = email
        user.bio = bio

        if avatar:
            user.avatar = avatar

        user.save()
        return redirect('profile', user_id=request.user.id)

    return render(request, "account/edit_profile.html", {"user": user})




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

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
    return render(request, 'posts/add_post.html', {'form': form})


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            # ✅ Редиректим на страницу поста после успешного добавления
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()

    return redirect('post_detail', pk=post.id)


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



def logout_view(request):
    logout(request)
    return redirect('accounts/login.html')
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('moder', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, blank=True)
    bio = models.CharField(null=True, blank=True, max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    content = models.CharField(null=True, blank=True)
    photos = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Groups(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    admins = models.ManyToManyField(User, related_name='admin_groups')
    members = models.ManyToManyField(User, related_name='member_groups')


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Очікує'), ('accepted', 'Прийнято'), ('rejected', 'Відхилено')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    file = models.FileField(upload_to='messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(
        max_length=20,
        choices=[
            ('message', 'Повідомлення'),
            ('friend_request', 'Запит у друзі'),
            ('like', 'Лайк'),
            ('comment', 'Коментар'),
        ]
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    score = models.PositiveSmallIntegerField(default=1)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    media = models.FileField(upload_to="comments", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Комментарий от {self.author} к посту "{self.post.title}"'
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput
from .models import User, Groups, Post, FriendRequest, Message, Notification, Rating,Chat, Comment

class UserFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photos']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'post']



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    birth_date = forms.DateField(label='Дата народження', widget=DateInput(attrs={'type': 'date'}))


    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Паролі не співпадають')
        return cd.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # важный момент — хэшируем пароль
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ім’я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ChatifyApp.models import User, Post, Groups, FriendRequest, Message, Notification, Rating, Chat, Comment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('username', 'avatar', 'bio', 'role')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Post)
admin.site.register(Groups)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Chat)
admin.site.register(Comment)



# Register your models here.

from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from LooplyApp.models import User, Post, Groups, FriendRequest, Message, Notification, Rating, Chat, Comment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'avatar_preview', 'email', 'username', 'role', 'bio', 'is_staff', 'is_active')
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
            'fields': (
                'email', 'username', 'password1', 'password2',
                'avatar', 'bio', 'role',
                'is_staff', 'is_active'
            ),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:40px; height:40px; border-radius:50%;" />', obj.avatar.url)
        return '—'
    avatar_preview.short_description = 'Аватар'


admin.site.register(Post)
admin.site.register(Groups)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Chat)
admin.site.register(Comment)


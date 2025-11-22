from django.urls import path
from . import views



urlpatterns = [
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('addposts/', views.add_post, name='addposts'),
    path('main/', views.main_view, name='main'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("profile-user/<int:user_id>/", views.profile_userView, name="profile_user"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
]


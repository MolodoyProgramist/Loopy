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
    
]


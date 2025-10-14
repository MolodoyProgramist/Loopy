from django.urls import path
from . import views



urlpatterns = [
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('main/', views.main_view, name='main'),
]

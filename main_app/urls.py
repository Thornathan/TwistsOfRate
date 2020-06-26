from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('consoles/', views.consoles_index, name='consoles_index'),
    path('consoles/<int:console_id>/', views.console_detail, name='console_detail'),
    path('games/<int:console_id>/add_console_comment/', views.add_console_comment, name='add_console_comment'),
    path('genres/', views.genres_index, name='genres_index'),
    path('genres/<int:genre_id>/', views.genres_detail, name='genres_detail'),
    path('games/', views.games_index, name='games_index'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('games/<int:game_id>/add_game_comment/', views.add_game_comment, name='add_game_comment'),
    path('blogs/', views.blogs_index, name='blogs_index'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/',  views.BlogCreate.as_view(), name='blogs_create'),
    path('blogs/<int:pk>/update/', views.BlogUpdate.as_view(), name='blogs_update'),
    path('blogs/<int:pk>/delete/', views.BlogDelete.as_view(), name='blogs_delete'),
    path('blogs/<int:blog_id>/add_blog_comment/', views.add_blog_comment, name='add_blog_comment'),
    path('blogs/<int:blog_id>/edit_blog_comment/<int:comment_id>/', views.edit_blog_comment, name='edit_blog_comment'),
    path('blogs/<int:blog_id>/delete_blog_comment/<int:comment_id>/', views.delete_blog_comment, name='delete_blog_comment'),
    path('accounts/signup/', views.signup, name='signup'),
]

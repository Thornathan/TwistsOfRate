from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('consoles/', views.consoles_index, name='consoles_index'),
    path('consoles/<int:console_id>/', views.console_detail, name='console_detail'),
    path('genre/', views.about, name='genre'),
    path('games/', views.games_index, name='games_index'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('blog/', views.about, name='blog'),
    path('accounts/signup/', views.signup, name='signup'),
]

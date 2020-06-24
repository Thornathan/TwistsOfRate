from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Console, Game, Blog
import uuid
import boto3
import requests

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def consoles_index(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/platforms"

  headers = {
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
    'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
    }

  response = requests.request("GET", url, headers=headers)
  consoles = Console.objects.all()
  return render(request, 'consoles/index.html', {'response': response, 'consoles': consoles })

def console_detail(request, console_id):
  url = "https://rawg-video-games-database.p.rapidapi.com/platforms/%7Bid%7D"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  console = Console.objects.get(id=console_id)
  return render(request, 'consoles/detail.html', {'response': response, 'console': console })

def games_index(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/games?page_size=200"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  games = response.json()['results']
  return render(request, 'games/index.html', {'games': games})

def game_detail(request, game_id):
  url = f"https://rawg-video-games-database.p.rapidapi.com/games/{game_id}"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  game = response.json()
  return render(request, 'games/detail.html', {'game': game })

def genres_index(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/genres?ordering=name"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  genres = response.json()['results']
  return render(request, 'genres/index.html', {'genres': genres})

def genres_detail(request, genre_id):

  url = f"https://rawg-video-games-database.p.rapidapi.com/genres/{genre_id}"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }
  response = requests.request("GET", url, headers=headers)
  genre = response.json()
  return render(request, 'genres/detail.html', {'genre': genre})

def blogs_index(request):
  blogs = Blog.objects.all()
  return render(request, 'blogs/index.html', { 'blogs': blogs })

def blog_detail(request, blog_id):
  blog = Blog.objects.get(id=blog_id)
  return render(request, 'blogs/detail.html', { 'blog': blog })



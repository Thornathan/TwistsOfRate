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
  url = "https://rawg-video-games-database.p.rapidapi.com/games"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  games = Game.objects.all()
  return render(request, 'games/index.html', {'response': response, 'games': games })

def game_detail(request, game_id):
  url = "https://rawg-video-games-database.p.rapidapi.com/games/%7Bgame_pk%7D"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  game = Game.objects.get(id=game_id)
  return render(request, 'games/detail.html', {'response': response, 'game': game })

def genres_index(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/genres"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  genre = Game.objects.get(genre=genre)
  return render(request, 'genres/index.html', {'response': response, 'genre': genre})

def genres_detail(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/genres/%7Bid%7D"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  genre = Game.objects.filter(genre=genre)
  return render(request, 'genres/detail.html', {'response': response, 'genre': genre})
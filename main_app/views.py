from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Console, Game, Blog, BlogComment, GameComment
from .forms import CommentForm, GCommentForm
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
  consoles = response.json()['results']
  return render(request, 'consoles/index.html', {'consoles': consoles })

def console_detail(request, console_id):
  url = f"https://rawg-video-games-database.p.rapidapi.com/platforms/{console_id}"

  headers = {
      'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
      'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
      }

  response = requests.request("GET", url, headers=headers)
  console = response.json()
  return render(request, 'consoles/detail.html', {'console': console })

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
  comments = GameComment.objects.filter(api_id=game_id)
  return render(request, 'games/detail.html', {'game': game, 'comments': comments })

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

def add_blog_comment(request, blog_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.blog_id = blog_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('blog_detail', blog_id=blog_id)

def add_game_comment(request, game_id):
  form = GCommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.api_id = game_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('game_detail', game_id=game_id)

class BlogCreate(LoginRequiredMixin, CreateView):
  model = Blog
  fields = ['title', 'body']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BlogUpdate(UpdateView):
  model = Blog
  fields = ['title', 'body']

class BlogDelete(DeleteView):
  model = Blog
  success_url = '/blogs/'

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Console, Game, Blog, BlogComment, GameComment, ConsoleComment
from .forms import CommentForm, GCommentForm, CCommentForm
import uuid
import boto3
import requests

# Create your views here.

def home(request):

  upcoming_games = "https://api.rawg.io/api/games?dates=2020-06-25,2020-10-10&page_size=6&ordering=-added"
  recent_releases = "https://api.rawg.io/api/games?dates=2020-05-20,2020-06-24&page_size=6&ordering=-added"
  highest_rated = "https://api.rawg.io/api/games?dates=2019-01-01,2019-12-31&page_size=6&ordering=-added"

  headers = {
    'x-rapidapi-host': "rawg-video-games-database.p.rapidapi.com",
    'x-rapidapi-key': "e623d7c465mshd3263eeaaa7033dp1631f8jsn581376b2f094"
    }

  ug_response = requests.request("GET", upcoming_games, headers=headers)
  rr_response = requests.request("GET", recent_releases, headers=headers)
  hr_response = requests.request("GET", highest_rated, headers=headers)

  games = ug_response.json()['results']
  releases = rr_response.json()['results']
  ratings = hr_response.json()['results']

  return render(request, 'home.html', {'games': games, 'releases': releases, 'ratings': ratings})

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
  comments = ConsoleComment.objects.filter(api_id=console_id)
  return render(request, 'consoles/detail.html', {'console': console, 'comments': comments })

def games_index(request):
  url = "https://rawg-video-games-database.p.rapidapi.com/games"

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
  user_id = request.user.id
  return render(request, 'blogs/detail.html', { 'blog': blog, 'user_id': user_id })

@login_required
def add_blog_comment(request, blog_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.blog_id = blog_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('blog_detail', blog_id=blog_id)

@login_required
def edit_blog_comment(request, comment_id):
  user_id = request.user.id
  return redirect('blog_detail', { 'comment_id':comment_id, 'user_id': user_id })

@login_required
def add_game_comment(request, game_id):
  form = GCommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.api_id = game_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('game_detail', game_id=game_id)

@login_required
def add_console_comment(request, console_id):
  form = CCommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.api_id = console_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('console_detail', console_id=console_id)

class BlogCreate(LoginRequiredMixin, CreateView):
  model = Blog
  fields = ['title', 'body']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BlogUpdate(LoginRequiredMixin, UpdateView):
  model = Blog
  fields = ['title', 'body']

class BlogDelete(LoginRequiredMixin, DeleteView):
  model = Blog
  success_url = '/blogs/'

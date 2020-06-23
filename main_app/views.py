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
  consoles = Console.objects.all()
  return render(request, 'consoles/index.html', { 'consoles': consoles })

def console_detail(request, console_id):
  console = Console.objects.get(id=console_id)
  return render(request, 'consoles/detail.html', { 'console': console })

def games_index(request):
  games = Game.objects.all()
  return render(request, 'games/index.html', { 'games': games })

def game_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  return render(request, 'games/detail.html', { 'game': game })


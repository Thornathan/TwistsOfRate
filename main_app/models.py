from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games_detail', kwargs={'pk':self.id})

class Console(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    release = models.DateField()
    games = models.ManyToManyField(Game)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'console_id': self.id})

class Blog(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField().auto_now
    body = models.TextField()
    console = models.ForeignKey(Console, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        
class BlogComment(models.Model):
    body = models.TextField(max_length=350)
    date = models.DateField(auto_now=True)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
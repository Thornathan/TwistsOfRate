from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Console(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    release = models.DateField()
    games = models.ManyToManyField(Game)
    
    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    body = models.TextField(max_length=6000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # new
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'blog_id': self.id})
        
class BlogComment(models.Model):
    body = models.TextField(max_length=350)
    date = models.DateField(auto_now=True)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

class GameComment(models.Model):
    body = models.TextField(max_length=350)
    date = models.DateField(auto_now=True)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_id = models.IntegerField()

    def __str__(self):
        return self.body

# New
class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"
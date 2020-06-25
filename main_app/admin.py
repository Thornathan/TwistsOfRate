from django.contrib import admin
from .models import Console, Game, Blog, BlogComment

# Register your models here.
admin.site.register(Console)
admin.site.register(Game)
admin.site.register(Blog)
admin.site.register(BlogComment)
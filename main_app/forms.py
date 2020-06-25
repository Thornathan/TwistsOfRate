from django.forms import ModelForm
from .models import BlogComment, GameComment


class CommentForm(ModelForm):
  class Meta:
    model = BlogComment
    fields = ['body']

class GCommentForm(ModelForm):
    class Meta:
        model = GameComment
        fields = ['body']


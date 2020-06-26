from django.forms import ModelForm
from .models import BlogComment, GameComment, ConsoleComment

class CommentForm(ModelForm):
  class Meta:
    model = BlogComment
    fields = ['body']

class GCommentForm(ModelForm):
    class Meta:
        model = GameComment
        fields = ['body']

class CCommentForm(ModelForm):
    class Meta:
        model = ConsoleComment
        fields = ['body']

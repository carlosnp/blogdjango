from django.shortcuts import render

# Create your views here.
from .models import Post
from django.http import HttpResponse
from django.views.generic import ListView

def posts_home(request):
    return HttpResponse("<h1>Hola</h1>")

class PostsListView(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

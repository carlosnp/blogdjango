from django.shortcuts import render

# Create your views here.
from .models import Post
from django.http import HttpResponse
from django.views.generic import ListView

def posts_create(request):
    return HttpResponse("<h1>Crear</h1>")

def posts_detail(request):
    return HttpResponse("<h1>Detalles</h1>")

def posts_list(request):
    return HttpResponse("<h1>Lista</h1>")

def posts_update(request):
    return HttpResponse("<h1>Actualizar</h1>")

def posts_delete(request):
    return HttpResponse("<h1>Borrar</h1>")

class PostsListView(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

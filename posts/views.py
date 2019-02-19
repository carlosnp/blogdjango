from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def posts_create(request):
	template_name = 'post_create.html'
	form = PostForm(request.POST or None)
	# if request.method == 'POST':
	# 	print(request.POST)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		return redirect("posts:list")
	context = {
		"form": form
	}
	return render(request, template_name, context)

def posts_detail(request, id):
	template_name = 'post_detail.html'
	instance = get_object_or_404(Post, id = id)
	context = {
		"title": "Detalles del Post",
		"instance": instance,
	}
	return render(request, template_name, context)

def posts_list(request):
	template_name = 'post_list.html'
	queryset = Post.objects.all()
	context = {
		"title": "Lista de Post",
		"object_list": queryset,
	}	
	# if request.user.is_authenticated:
	# 	context = {
	# 		"title": "Autenticado"
	# 	}
	# else:
	# 	context = {
	# 		"title": "Lista"
	# 	}
	return render(request, template_name, context)

def posts_update(request):
    return HttpResponse("<h1>Actualizar</h1>")

def posts_delete(request):
    return HttpResponse("<h1>Borrar</h1>")


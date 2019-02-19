from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from .forms import PostForm

def posts_create(request):
	template_name = 'post_create.html'
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Felicidades creaste un Post")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Algo salio mal, no se creo el Post")
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
	return render(request, template_name, context)

def posts_update(request, id=None):
    template_name = 'post_create.html'
    instance = get_object_or_404(Post, id = id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
    	instance = form.save(commit = False)
    	print(form.cleaned_data.get("title"))
    	instance.save()
    	messages.success(request, "Actualizaste el Post")
    	return redirect("posts:detail", id=id)
    context = {
    	"title": instance.title,
    	"instance": instance,
    	"form": form,
    }
    return render(request, template_name, context)

def posts_delete(request):
    return HttpResponse("<h1>Borrar</h1>")


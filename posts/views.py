# Django
from django.contrib.contenttypes.models import ContentType
from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

# Project
from .models import Post
from .forms import PostForm
from comments.models import Comment

def posts_create(request):
	
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	
	template_name = 'post_create.html'
	form = PostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		instance = form.save(commit = False)
		instance.author = request.user
		instance.save()
		messages.success(request, "Felicidades!!! creaste el POST: %s" % instance.title)
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title": "Create Post",
		"titles": "Crear Post",
		"form": form
	}
	return render(request, template_name, context)

def posts_detail(request, id):
	
	template_name = 'post_detail.html'
	instance = get_object_or_404(Post, id = id)
	
	# permite ver los post que son borradores y su fecha de publicacion es mayor a la actual
	if instance.draf or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	
	share_string = quote_plus(instance.content)
	
	content_type = ContentType.objects.get_for_model(Post)
	obj_id 		 = instance.id
	comments 	 = Comment.objects.filter(content_type = content_type, object_id = obj_id)

	context = {
		"title": "Detalles del Post",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
	}
	return render(request, template_name, context)

def posts_list(request):
	template_name = 'post_list.html'
	# El filtro active fue definido en el modelo
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	# si es un usuario o un superusuario mostrara todos los posts
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()		
	# Buscador
	query = request.GET.get("q")
	if query:
		# Filtro de busqueda
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(author__first_name__icontains=query) |
			Q(author__last_name__icontains=query))
	# Paginacion
	paginator = Paginator(queryset_list, 6)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	#page = request.GET.get('page')
	
	try:
		#queryset = paginator.get_page(page)
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	
	context = {
		"title": "Lista de Post",
		"object_list": queryset,
		"page_request_var": page_request_var,
		"today": today,
	}	
	return render(request, template_name, context)

def posts_update(request, id=None):
    
    if not request.user.is_staff or not request.user.is_superuser:
    	raise Http404
    
    template_name = 'post_create.html'
    instance = get_object_or_404(Post, id = id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    
    if form.is_valid():
    	instance = form.save(commit = False)
    	instance.save()
    	messages.success(request, "Actualizaste el POST: %s" % instance.title)
    	return redirect("posts:detail", id=id)
    
    context = {
    	"title": instance.title,
    	"titles": "Editar Post",
    	"instance": instance,
    	"form": form,
    }
    return render(request, template_name, context)

def posts_delete(request, id=None):
	instance = get_object_or_404(Post, id = id)
	instance.delete()
	messages.success(request, "Eliminaste el Post")
	return redirect("posts:list")
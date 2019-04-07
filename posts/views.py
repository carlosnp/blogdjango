# Django
from urllib.parse import quote_plus
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Project
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment

@login_required(login_url='accounts:login')
def posts_create(request):
	template_name = 'post_create.html'
	
	# Permisos para crear posts
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	#raise Http404
	# 	template_names 	= "403.html"
	# 	contextdata = {}
	# 	return render(request, template_names, contextdata, status = 403)
	
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
	# instance = get_object_or_404(Post, id = id)
	try:
		instance = Post.objects.get(id=id)
	except:
		#raise Http404
		template_names 	= "404.html"
		detail_comment = "El post que buscas no existe"
		contextdata = {
			"detail_comment": detail_comment,
		}
		return render(request, template_names, contextdata, status = 404)
	
	# permite ver los post que son borradores y su fecha de publicacion es mayor a la actual
	if instance.draf or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			#raise Http40
			template_names 	= "404.html"
			contextdata = {}
			return render(request, template_names, contextdata, status = 404)
	
	share_string = quote_plus(instance.content)
	
	# Contador de palabras

	# Base de Datos inicial
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id,
	}
	# Crea comentarios
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated:
		c_type 			= form.cleaned_data.get("content_type")
		content_type 	= ContentType.objects.get(model=c_type)
		obj_id 			= form.cleaned_data.get("object_id")
		content_data 	= form.cleaned_data.get("content")
		
		# Verificamos si existe el padre de un comentario
		parent_obj		= None
		try:
			parent_id	= int(request.POST.get("parent_id"))
		except:
			parent_id	= None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs[0] #.first()

		# Creamos un comentario
		new_comment, created = Comment.objects.get_or_create(
										author = request.user,
										content_type = content_type,
										object_id= obj_id,
										content=content_data,
										parent = parent_obj
										)
		if created:
			messages.success(request, "Añadiste un comentario al POST: %s" % instance.title)

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	# Muestra comentarios
	comments = instance.comments

	context = {
		"title": "Detalles del Post",
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form
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
	# Buscar en la lista de POST
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

@login_required(login_url='accounts:login')
def posts_update(request, id=None):
    template_name = 'post_create.html'
    
    #instance = get_object_or_404(Post, id = id)
    try:
    	instance = Post.objects.get(id=id)
    except:
    	template_names 	= "404.html"
    	detail_comment = "El Post que buscas no existe"
    	contextdata = {
    		"detail_comment": detail_comment,
    	}
    	return render(request, template_names, contextdata, status = 404)
    
    # if not request.user.is_staff or not request.user.is_superuser:
    # 	#raise Http404
    # 	template_names 	= "403.html"
    # 	contextdata = {}
    # 	return render(request, template_names, contextdata, status = 403)

    # Si el usuario y el autor del posts no coninciden
    if instance.author != request.user:
    	template_name 	= "403.html"
    	detail_comment = "Opsss!!!"
    	content_text = instance.title
    	contextdata = {
    		"detail_comment": detail_comment,
			"content_text": content_text,
			"userlogin": request.user,
			"editall": True,
		}
    	return render(request, template_name, contextdata, status = 403)
    
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
    	"form": form
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def posts_delete(request, id=None):
	#instance = get_object_or_404(Post, id = id)
	try:
		instance = Post.objects.get(id=id)
	except:
		#raise Http404
		template_names 	= "404.html"
		detail_comment = "No Existe el post que deseas Eliminar"
		contextdata = {
			"detail_comment": detail_comment,
		}
		return render(request, template_names, contextdata, status = 404)

	if instance.author != request.user:
		template_name 	= "403.html"
		detail_comment = "Opsss!!!"
		content_text = instance.title
		contextdata = {
			"detail_comment": detail_comment,
			"userlogin": request.user,
			"content_text": content_text,
			"deleteall": True,
		}
		return render(request, template_name, contextdata, status = 403)

	instance.delete()
	messages.success(request, "Eliminaste el Post: %s" % instance.title)
	return redirect("posts:list")
# Django
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Autentificacion django
from django.contrib.auth import authenticate, get_user_model, login, logout
# Project
from .forms import UserLoginForm, UserRegisterForm

def loginView(request):
	template_name = "loginform.html"
	next = request.GET.get("next")
	title = "Iniciar Sesión" # Login
	form = UserLoginForm(request.POST or None)
	# Si el formulario es valido
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user	 = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
			messages.success(request, "Bienvenido!! %s" % request.user)
		if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
			messages.success(request, "Bienvenido!! STAFF %s" % request.user)
		if request.user.is_active and request.user.is_staff and request.user.is_superuser:
			messages.success(request, "Bienvenido!! SUPERUSUARIO %s" % request.user)
		return redirect("posts:list")
	# Context Data
	context = {
		"title": title,
		"form": form
	}
	return render(request, template_name, context)

def registerView(request):
	template_name = "loginform.html"
	next = request.GET.get("next")
	title = "Registro de Usuario"
	form = UserRegisterForm(request.POST or None)
	# Verificamos si el formulario es valido
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		# Guardamos la informacion del usuario
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect("posts:list")
	# Context Data
	context = {
		"title": title,
		"form": form
	}
	return render(request, template_name, context)

def logoutView(request):
	#template_name = "/"
	#context = {}
	logout(request)
	return redirect("posts:list")
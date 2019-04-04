# Django
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Autentificacion django
from django.contrib.auth import authenticate, get_user_model, login, logout
# Project
from .forms import UserLoginForm

def loginView(request):
	template_name = "loginform.html"
	title = "Iniciar Sesión" # Login
	form = UserLoginForm(request.POST or None)
	# Si el formulario es valido
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
	# Context Data
	context = {
		"title": title,
		"form": form
	}
	return render(request, template_name, context)

def registerView(request):
	template_name = "loginform.html"
	context = {}
	return render(request, template_name, context)

def logoutView(request):
	template_name = "loginform.html"
	context = {}
	return render(request, template_name, context)
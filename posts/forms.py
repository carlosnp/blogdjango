# Django
from django import forms
# Django External APP
from pagedown.widgets import PagedownWidget
# Project
from .models import Post

class PostForm(forms.ModelForm):
	# Formulario de Contenido
	content = forms.CharField(label="Contenido",widget=PagedownWidget(show_preview=False))
	# Formulario de Fecha con un select
	publish = forms.DateField(label="Publicar el",widget=forms.SelectDateWidget)
	class Meta:
		model = Post
		fields = ["title", "content", "image", "draf", "publish","author"]
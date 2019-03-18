# Django
from django import forms
# Project
from .models import Comment

class CommentForm(forms.Form):
    content_type 	= forms.CharField(
    				label="Tipo de Contenido",
    				widget=forms.HiddenInput)
    object_id 		= forms.IntegerField(
    				label="ID", 
    				widget=forms.HiddenInput)
    # parent_id 		= forms.IntegerField(label="ID", widget=forms.HiddenInput, required=False)
    contetn 		= forms.CharField(
    				label="Comentario", 
    				widget=forms.Textarea)
    
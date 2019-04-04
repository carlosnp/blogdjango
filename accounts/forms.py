# Django
from django import forms
# Autentificacion django
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username    = self.cleaned_data.get("username")
        password    = self.cleaned_data.get("password")
        
        # user_qs     = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
        	user = authenticate(username=username, password=password)
	        # Si no existe el usuario
	        if not user:
	            raise forms.ValidationError("El usuario no existe")
	        # Si la contraseña no coincide
	        if not user.check_password(password):
	            raise forms.ValidationError("Contraseña Incorrecta")
	        # Si el usuario no esta activo
	        if not user.is_active:
	            raise forms.ValidationError("El usuario no esta activo")
        # Retorno
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Dirección de correo electrónico')
	email2 = forms.EmailField(label='Confirme la Dirección de correo electrónico')
	password = forms.CharField(label='Contraseña',widget=forms.PasswordInput)	
	class Meta:
		model 	= User
		fields 	= [
			'username',
			'email',
			'email2',
			'password'
		]
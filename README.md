# blogdjango
Para instalar la aplicación en modo desarrollo debera seguir los siguientes pasos:
===========================================================

1-) Instalar el controlador de versiones git:
------------------------------------------------------
    
    Ingresar como super usuario:

    $ su

    # aptitude install git
    
    Salir del modo super usuario

2-) Descargar el codigo fuente del proyecto:

$ git clone https://github.com/carlosnp/blogdjango.git

3-) Crear un Ambiente Virtual:
El proyecto está desarrollado con el lenguaje de programación Python, se debe instalar Python 3.6.7

4.- Luego de instalar el ambiente virtual:

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic 
$ python manage.py runserver

5.- Para probar el token

Debes instalar:
$ sudo apt install curl

Iniciar el servidor de python:
$ python manage.py runserver

TEST: 
Luego en otro terminal:
$ curl -X POST -d "username=hansolo&password=1234comun" http://127.0.0.1:8000/api/accounts/token/

Respondera algo asi
{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImNhcmxvcyIsImV4cCI6MTU1NTc2NTI0NywiZW1haWwiOiJjYXJsb3NAbm9zZXNhYmUuY29tIn0.p6PpKEljAwZLmdD-7WyLVj8lrH_Z_JSgKGhAT0qIomU"}

$ curl http://127.0.0.1:8000/api/comments/

Lista de post
$ curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImhhbnNvbG8iLCJleHAiOjE1NTU3NjU3NDksImVtYWlsIjoiaGFuQHNvbG8uY29tIn0.nlk9huYr1lxHYhV27fFmPhq9Q67nGsf_yI6Ry9tgY34" http://127.0.0.1:8000/api/posts/


Para crear un comentario
$ curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImhhbnNvbG8iLCJleHAiOjE1NTU3NjY3NDksImVtYWlsIjoiaGFuQHNvbG8uY29tIn0.3T7rdcYXbtJlYqSskXDSLJaOXcWNG6PGJ17HOFKHRO8" http://127.0.0.1:8000/api/comments/create/?type=post&slug=hola-soy-leia-organa

$ curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImhhbnNvbG8iLCJleHAiOjE1NTU3NjY3NDksImVtYWlsIjoiaGFuQHNvbG8uY29tIn0.3T7rdcYXbtJlYqSskXDSLJaOXcWNG6PGJ17HOFKHRO8" -X POST -d "content=Contenido de prueba desde django rest" http://127.0.0.1:8000/api/comments/create/?type=post&slug=hola-soy-leia-organa


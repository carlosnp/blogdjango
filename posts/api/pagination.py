# Paginacion Django Rest Framework
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)

class PostLimitOffsetPagination(LimitOffsetPagination):
	default_limit = 3 # límite a utilizar si el cliente no proporciona uno en un parámetro de consulta
	# limit_query_param = 3 # número máximo de artículos a devolver
	# offset_query_param = 10 # posición inicial de la consulta en relación con el conjunto completo de elementos no paginados.
	max_limit = 10 # límite máximo permitido que puede solicitar el cliente

class PostPageNumberPagination(PageNumberPagination):
	page_size = 5 #  indica el tamaño de la página
	# page_query_param
	# page_size_query_param
	# max_page_size = 1000 # indica el tamaño de página máximo permitido permitido
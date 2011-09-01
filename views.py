#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
import sys

sys.path.append('srcp')
sys.path.append('srcp/dj_DAO')

import valoracion
import daoValoracion
import daoPelicula
from srcp.models import Pelicula, Usuario, Valoracion, Similitud

class CSRPError(Exception):
	
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

def login(request):
	""" Función para realizar el login

	Params:

		request(): 

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	context['title'] = 'Login'
	
	try:
		
		if 'login_button' not in request.POST:
			raise CSRPError('Login incorrecto')
	
		u = Usuario.objects.get(idUsu=request.POST['idUsu'])
	
		if u.clave == request.POST['clave']:
			
			request.session['idUsu'] = u.idUsu
			request.session['nvaloraciones'] = 0
			request.session['nuevasValoraciones'] = []
			
			response_page = 'srcp/index.html'
		
		else:
			
			raise CSRPError('Login incorrecto')
	
	except (CSRPError, ValueError, Usuario.DoesNotExist):
	
		context['error'] = "Login incorrecto"
		response_page = 'srcp/login.html'
	
	finally:
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))

def logout(request):
	""" Función para cerrar sesión

	Params:

		request():

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	try:
		
		__checkIsLogged(request)

		if 'logout_button' in request.POST:
			
			del request.session['idUsu']
			
			context['title'] = 'Login'
			response_page = 'srcp/login.html'
			
		else:
			
			response_page = 'srcp/index.html'
			context['error'] = 'Error al cerrar sesión'
			context['title'] = 'Índice'
		
	except KeyError:
		
		response_page = 'srcp/login.html'
	
	# Error de login
	except CSRPError:
		
		context['titulo'] = 'Login'
		response_page = 'srcp/login.html'

	finally:
		
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))

def indice(request):
	""" Función para cuando se hace la peticion de index.html o de la raíz

	Params:

		request():

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	try:
		
		__checkIsLogged(request)
		
		context['titulo'] = 'Índice'
		response_page = 'srcp/index.html'
		
		#estra_pred = None
		#recomendaciones = self.recomendar(estra_pred)
		
		#context['recomendaciones'] = recomendaciones
	
	# Error de login
	except CSRPError:
		
		context['titulo'] = 'Login'
		response_page = 'srcp/login.html'
	
	finally:
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))

def valorar(request, idPel):
	""" Función para valorar una película

	Params:

		request():
		idPel: id de la película valorada

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	try:
		
		__checkIsLogged(request)
	
		idUsu = request.session['idUsu']
		
		#print idUsu, '-->', idPel, '-->', int(request.POST['puntuacion'])
		
		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)
		punt = int(request.POST['puntuacion'])
		
		#redirected_view = 'srcp.views.buscar'
		
	except (KeyError, Valoracion.DoesNotExist):
	
		# Redisplay the poll voting form.
		#context['pelicula'] = p
		
		#context['error'] = "Error al valorar la película."
		#response_page = 'srcp/index.html'
		
		redirected_view = 'srcp.views.buscar'
		
	except CSRPError:
		
		#context['titulo'] = 'Login'
		#response_page = 'srcp/login.html'
		
		#return render_to_response(response_page, context, \
									#context_instance=RequestContext(request))
									
		redirected_view = 'srcp.views.login'
	
	else:
		
		v = valoracion.Valoracion(idUsu=usu.idUsu, idPel=pel.idPel, \
															valoracion=punt)
		daov = daoValoracion.DAOValoracion()
		daov.inserta(v)
		
		request.session['nuevasValoraciones'].append(v)
		
		# Cuando el nº de inserciones sea 5, actualizamos el modelo
		request.session['nvaloraciones'] += 1
		
		if request.session['nvaloraciones'] == 5:
			
			self.__actualizarModelo()
			
			request.session['nvaloraciones'] = 0
			
		redirected_view = 'srcp.views.buscar'
	
	finally:
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse(redirected_view))#'srcp.views.buscar'))

def buscar(request):
	""" Función para buscar las películas con el nombre dado

	Params:

		request():

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	try:
	
		__checkIsLogged(request)
		
		response_page = 'srcp/index.html'

		if 'busqueda' in request.POST:
			busqueda = request.POST['busqueda']
			request.session['ult_busq'] = busqueda
			
		else: # para cuando sea redirigido desde una valoración
			busqueda = request.session['ult_busq']
			
		#daop = daoPelicula.DAOPelicula()
		
		#pels = daop.getPeliculasTitulo(busqueda)
		
		#for p in pels:
			#pel = Pelicula(idPel=p.idPel, titulo=p.titulo, anio=p.anio)
			#context['peliculas'].append(p)
		
		#context['idUsu'] = request.session['idUsu']
		context['peliculas'] = []
		
		vals = Valoracion.objects.filter( Usu=request.session['idUsu'])
		
		for p in Pelicula.objects.filter( titulo__contains=busqueda):
			
			try:
				
				val = vals.get(Pel=p).puntuacion
			
			except Valoracion.DoesNotExist:
				
				val = 0
				
			finally:
				
				context['peliculas'].append((p, val))
			
		
	# Error de login
	except CSRPError:
		
		context['titulo'] = 'Login'
		response_page = 'srcp/login.html'
	
	finally:
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))
	
def get_recomendaciones(request):
	""" Función para obtener las recomendaciones

	Params:

		request():
		idPel: id de la película valorada

	Return:

		(Nonetype): None
	"""
	
	daop = daoPelicula.DAOPelicula()
	
	# devuelve una lista de idPel, de aquellas películas no puntuadas por ese usuario
	lpelnop = daop.getPeliculasNoPuntuadas(request.session['idUsu'])
	
	# Creamos una lista de valores predichos
	lvalpred = []
	
	for idPel in lpelnop:
		prediccion = estra_pred.predice(request.session['idUsu'], idPel)
		val = valoracion.Valoracion(request.session['idUsu'], idPel, prediccion)
		lvalpred.append(val)
	
	# Ordenamos los elementos "Valoraciones", de forma descendente y por el valor de la puntación
	lvalpred.sort(reverse=True)
	
	return lvalpred[:5]
	

def __actualizarModelo(self): # Para javi
	""" Método para actualizar el modelo tras haber nuevas valoraciones

	Params:

		None

	Return:

		None
	"""
	
	valoraciones = []
	
	#obtener valoraciones de todas las películas puntuadas
	for v in request.session['nuevasValoraciones']:
		valoraciones += self.getValoracionesItem(v.idPel).values()#----------------------------------------DAO----------
	
	eSimilitud = estrategiaSimilitud.EstrategiaSimilitud()
	eSimilitud.actualizaSimilitud(valoraciones, self.__nuevasValoraciones)

	
def __checkIsLogged(request):
	
	if 'idUsu' not in request.session:
		
		raise CSRPError('No estás logueado')
		

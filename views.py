#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

import threading
import sys

sys.path.append('srcp')
sys.path.append('srcp/estrategiasSimilitud')
sys.path.append('srcp/estrategiasPredicción')
sys.path.append('srcp/dj_DAO')

import pearson
import agrupamiento
import weithedSum
import itemAvgAdj1
import itemAvgAdjN
import valoracion
import daoValoracion
import daoParSimilitud
import daoPelicula
import estrategiaSimilitud
import estrategiaPrediccion
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
	context['error'] = ''
	
	try:
		
		if 'login_button' not in request.POST:
			raise CSRPError('Login incorrecto')
	
		u = Usuario.objects.get(idUsu=request.POST['idUsu'])
		
		if u.clave == request.POST['clave']:
			
			request.session['idUsu'] = u.idUsu
			request.session['nvaloraciones'] = 0
			request.session['nuevasValoraciones'] = []
			request.session['recomendaciones'] = get_recomendaciones(request.session['idUsu'])
			
			#response_page = 'srcp/index.html'
			redirected_view = 'srcp.views.indice'
			
		else:
			
			raise CSRPError('Login incorrecto')
	
	except (CSRPError, ValueError, Usuario.DoesNotExist):
	
		context['error'] = "Login incorrecto"
		response_page = 'srcp/login.html'
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))
									
	else:
		
		return HttpResponseRedirect(reverse(redirected_view))

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
		context['recomendaciones'] = request.session['recomendaciones']
		response_page = 'srcp/index.html'
		
	# Error de login
	except CSRPError:
		
		context['titulo'] = 'Login'
		response_page = 'srcp/login.html'
		
	except Exception, ex:
		
		print "Excepción inesperada:", ex
	
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

		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)

		for k in request.POST.keys():
			if 'estrella' in k:
				punt = k[9:10]
				punt = int(punt)
				break
		
	except (KeyError, Valoracion.DoesNotExist):
	
		redirected_view = 'srcp.views.buscar'
		
	except CSRPError:
		
		redirected_view = 'srcp.views.login'
		
	else:
		
		v = valoracion.Valoracion(idUsu=usu.idUsu, idPel=pel.idPel, \
															valoracion=punt)
		daov = daoValoracion.DAOValoracion()
		daov.inserta(v)
		
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
		
		context['recomendaciones'] = request.session['recomendaciones']
		response_page = 'srcp/index.html'
		
		# Si no se ha hecho ninguna búsqueda, se hace la anterior
		if 'busqueda' in request.POST:
			busqueda = request.POST['busqueda']
			request.session['ult_busq'] = busqueda
			
		else: # para cuando sea redirigido desde una valoración
			busqueda = request.session['ult_busq']
			
		context['peliculas'] = []
		
		vals = Valoracion.objects.filter( Usu=request.session['idUsu'])
		
		res_busq = Pelicula.objects.filter(titulo__icontains=busqueda)
		
		context['num_peliculas'] = len(res_busq)
		
		for p in res_busq[:100]:
			
			try:
				
				val = vals.get(Pel=p).puntuacion
			
			except Valoracion.DoesNotExist:
				
				val = 0
				
			finally:
				
				context['peliculas'].append((p, val))
			
		
	# Error de login
	except CSRPError:
		
		context['titulo'] = 'Login'
		context['error'] = "Sesión no iniciada"
		response_page = 'srcp/login.html'
	
	finally:
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))
	
def get_recomendaciones(idUsu):
	""" Función para obtener las recomendaciones

	Params:

		idUsu: idUsu del usuario al que se le recomienda

	Return:

		(list): peliculas recomendadas (Pelicula, clase django)
	"""
	
	daop = daoPelicula.DAOPelicula()
	daov = daoValoracion.DAOValoracion()
	daops = daoParSimilitud.DAOParSimilitud()
	estra_pred = weithedSum.WeithedSum()
	agrup = agrupamiento.Agrupamiento()
	
	lpelnop = daop.getPeliculasNoPuntuadas(idUsu)[:1000]
	lvalpred = []
	k = 30

	for p in lpelnop:
		valsUsu = daov.getValoracionesUsuario(idUsu)
		simsItem = daops.getSimilitudesItem(p.idPel)

		# Calculamos los k-vecinos más cercanos a ese elemento (con máximo "k")
		kmaxValVec = agrup.agrupknn(simsItem, valsUsu, p.idPel, 30)
		
		prediccion =  estra_pred.predice(simsItem, idUsu, p.idPel, kmaxValVec[:k])
		lvalpred.append(prediccion)
	
	# Ordenamos los elementos "Valoraciones", de forma descendente y por el valor de la puntación
	
	lvalpred.sort(reverse=True) #, cmp=valoracion.cmp_val)
	
	pels_rec = []
	
	for v in lvalpred[:5]:
		pels_rec.append(daop.getPelicula(v.idPel))
	
	return pels_rec
	#return daop.getPeliculasNoPuntuadas(idUsu)[200:205]

def __crearModelo(estrat_sim=None):
	""" 

	Params:

		PARAM(): DESCRIPTION

	Return:

		(): DESCRIPTION
	"""
	if not estrat_sim:
		estrat_sim = estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)

	estrat_sim.similitud()
	
def __checkIsLogged(request):
	
	if 'idUsu' not in request.session:
		
		raise CSRPError('No estás logueado')
		

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
	
	try:
		
		if 'login_button' not in request.POST:
			raise CSRPError('Login incorrecto')
	
		u = Usuario.objects.get(idUsu=request.POST['idUsu'])
	
		if u.clave == request.POST['clave']:
			
			request.session['idUsu'] = u.idUsu
			request.session['nvaloraciones'] = 0
			request.session['nuevasValoraciones'] = []
			
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
		context['recomendaciones'] = get_recomendaciones(request.session['idUsu'])
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

		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)

		for k in request.POST.keys():
			if 'estrella' in k:
				punt = k[9:10]
				punt = int(punt)
				break
		
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
		
		if request.session['nvaloraciones'] >= 5:
			print "--> Se han hecho >=5 valoraciones, es momento de actualizar"
			
			__actualizarModelo(request)

			print "--> Modelo actualizandose"
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
		
		context['recomendaciones'] = get_recomendaciones(request.session['idUsu'])
		response_page = 'srcp/index.html'
		
		# Si no se ha hecho ninguna búsqueda, se hace la anterior
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
		
		for p in Pelicula.objects.filter( titulo__icontains=busqueda):
			
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
	
	else:
	
		return render_to_response(response_page, context, \
									context_instance=RequestContext(request))
	
def get_recomendaciones(idUsu):
	""" Función para obtener las recomendaciones

	Params:

		idUsu: idUsu del usuario al que se le recomienda

	Return:

		(list): peliculas recomendadas (Pelicula, clase django)
	"""
	print "Entra get_recomendaciones"
	daop = daoPelicula.DAOPelicula()
	#daops = daoParSimilitud.DAOParSimilitud()
	#lpelnop = daop.getPeliculasNoPuntuadas(idUsu)
	#estra_pred = weithedSum.WeithedSum()

	## Creamos una lista de valores predichos
	#lvalpred = []

	#for p in lpelnop:
		#print "idPel", p.idPel
		#sims = daops.getSimilitudesItem(p.idPel)
		#print 11
		
		#tn = (2, 4, 8)
		#tep = [( "Item Average Adjustment All-1", itemAvgAdj1.ItemAvgAdj1())]
		#for n in tn:
			#tep.append(( "Item Average Adjustment n = " + str(n), itemAvgAdjN.ItemAvgAdjN(n)))
		#tep.append(( "Weighted Sum", weithedSum.WeithedSum()))
		
		#val = estra_pred.predice(sims, idUsu, p.idPel, tep)
		#print 12
		#lvalpred.append(val)
		#print "13"
		
	## Ordenamos los elementos "Valoraciones", de forma descendente y por el valor de la puntación
	#lvalpred.sort(reverse=True)

	#return lvalpred[:5]
	return daop.getPeliculasNoPuntuadas(idUsu)[:5]

def __crearModelo(estrat_sim=None):
	""" 

	Params:

		PARAM(): DESCRIPTION

	Return:

		(): DESCRIPTION
	"""
	print "Se entra en __crearModelo"
	if not estrat_sim:
		estrat_sim = estrategiaSimilitud.EstrategiaSimilitud(pearson.calcula_similitud)
	print "Se llama a la estrategia de similitud"
	estrat_sim.similitud()
	
def __checkIsLogged(request):
	
	if 'idUsu' not in request.session:
		
		raise CSRPError('No estás logueado')
		

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
#from django.template import RequestContext
import sys

sys.path.append('dj_DAO')

import valoracion
import daoValoracion
import daoPelicula
from srcp.models import Pelicula, Usuario, Valoracion, Similitud


def login(request):
	""" Función para realizar el login

	Params:

		request(): 

	Return:

		(Nonetype): None
	"""
	
	
	u = Usuario.objects.get(username__exact=request.POST['nombre'])
	context = {}
	
	if u.clave == request.POST['clave']:
		
		request.session['idUsu'] = m.idUsu
		
		return render_to_response('srcp/indice.html', context)
	
	else:
		
		context['error'] = 'Login incorrecto'
		
		return render_to_response('srcp/login.html', context)

def logout(request):
	""" Función para cerrar sesión

	Params:

		request():

	Return:

		(Nonetype): None
	"""
	
	context = {}
	
	try:
		
		del request.session['idUsu']
		
		return render_to_response('srcp/login.html', context)
		
	except KeyError:
		
		pass
	
	finally:

		return HttpResponse("Ha cerrado sesión.")

def indice(request):
	""" Función para cuando se hace la peticion de index.html

	Params:

		request():

	Return:

		(Nonetype): None
	"""

	estra_pred = None
	recomendaciones = self.recomendar(estra_pred)
	
	context = {
		'recomendaciones': recomendaciones
	}
	
	return render_to_response('srcp/index.html', context)

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
		
		idUsu = request.session['idUsu']
			
		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)
		punt = int(request.POST['puntuacion'])
		daov = daoValoracion.DAOValoracion()
		
	except (KeyError, Valoracion.DoesNotExist):
	
		# Redisplay the poll voting form.
		#context['pelicula'] = p
		context['error'] = "Error al valorar la película."
		
		return render_to_response('srcp/indice.html', context)
	
	else:
	
		v = valoracion.Valoracion(idUsu=usu.idUsu, idPel=pel.idPel, \
															valoracion=punt)
		
		daov.inserta(v)

		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('srcp.views.results', args=(p.id,)))

def buscar(request):
	""" Función para buscar las películas con el nombre dado

	Params:

		request():

	Return:

		(Nonetype): None
	"""
	
	busqueda = request.POST['busqueda']
	daop = daoPelicula.DAOPelicula()
	context = {}
	
	pels = daop.getPeliculasTitulo(busqueda)
	context['peliculas'] = []
	
	for p in pels:
		pel = Pelicula(idPel=p.idPel, titulo=p.titulo, anio=p.anio)
		context['peliculas'].append(p)
	
	return render_to_response('srcp/index.html', context)

def get_recomendaciones(request):
	""" Función para obtener las recomendaciones

	Params:

		request():
		idPel: id de la película valorada

	Return:

		(Nonetype): None
	"""
	
	pass

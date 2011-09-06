#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from singleton import *

#import parSimilitud
#import valoracion
import pelicula
import daoValoracion
import srcp.models as djModels


class DAOPelicula(Singleton):
	""" Class doc """
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getPeliculas(self):
		""" Devuelve todas las peliculas con las que se trabaja
	
		Params:
	
			None
	
		Return:
	
			(list): Lista con objetos Pelicula
		"""
		
		djPeliculas = djModels.Pelicula.objects.all()
		
		pelis=[]
		
		for djp in djPeliculas:
		
			p = pelicula.Pelicula(titulo=djp.titulo, idPel=djp.idPel, anio=djp.anio)
			pelis.append(p)
		
		return pelis
	
	def getPeliculasTitulo(self,tit):
		"""
		Busca entre todas las peliculas aquellas que coinciden con el titulo proporcionado
		Params:
			tit: titulo de la pelicula a buscar
		"""		
		
		djPeliculas = djModels.Pelicula.objects.filter(titulo__icontains=tit)
		
		pelis=[]
		
		for djp in djPeliculas:
			
			p = pelicula.Pelicula(titulo=djp.titulo, idPel=djp.idPel, anio=djp.anio)
			pelis.append(p)
			
		return pelis
	
	def getPelicula(self,id):
		"""
		Busca la pelicula que coincide exactamente con el id suministrado
		Params:
			id: id de la película a devolver
		"""
		
		peli = None
		
		try:
			
			djp = djModels.Pelicula.objects.get(idPel=id)
			
			peli = pelicula.Pelicula(titulo=djp.titulo, idPel=djp.idPel, anio=djp.anio)
			
		except djModels.Pelicula.DoesNotExist:
	
			pass
			
		finally:
	
			return peli
	
	def getPeliculasNoPuntuadas(self,idUsu):
		"""
		Para un usuario concreto devuelve aquellas películas que no han sido valoradas
		Params:
			idUsu: usuario cuyas peliculas no valoradas se van a buscar
		"""
		
		daov = daoValoracion.DAOValoracion()
		
		vals = daov.getValoracionesUsuario(idUsu)
		
		djPels = djModels.Pelicula.objects.all()

		for v in vals:
			djPels = djPels.exclude(idPel=v.idPel)
		
		pelis = []
		
		for djp in djPels:
			p = pelicula.Pelicula(titulo=djp.titulo, idPel=djp.idPel, anio=djp.anio)
			pelis.append(p)
		
		return pelis
		

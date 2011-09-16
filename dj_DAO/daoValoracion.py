#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from singleton import *

import valoracion
import srcp.models as djModels


class DAOValoracion(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialisera """
		
		pass

	def getValoraciones(self):
		""" Método que devuelve todas las valoraciones realizadas
	
		Params:
	
			None
	
		Return:
	
			(list): Lista de objetos Valoracion
		"""
		
		djVals = djModels.Valoracion.objects.all()
		
		valoraciones = []
		
		for djv in djVals:
			
			v = valoracion.Valoracion(idUsu=djv.Usu.idUsu, idPel=djv.Pel.idPel, \
													valoracion=djv.puntuacion)
			valoraciones.append(v)
		
		return valoraciones

	
	def getValoracionesUsuario(self,idUsu):
		""" obtiene las valoraciones para todas las peliculas de un usuario concreto
		params:
			idUsu: identificador del usuario
		"""
		
		djVals = djModels.Valoracion.objects.filter(Usu=idUsu)
		
		valoraciones = []
		
		for djv in djVals:
			
			v = valoracion.Valoracion(idUsu=djv.Usu.idUsu, idPel=djv.Pel.idPel, \
													valoracion=djv.puntuacion)
			valoraciones.append(v)
		
		return valoraciones
	
	def getValoracionesItem(self,idPel):
		""" Obtiene las valoraciones que todos los usuarios han realizado sobre una pelicula concreta
		
		Params:
			idPel: identificador de la pelicula
			
		Return:
			lista con las valoraciones
		"""
		djVals = djModels.Valoracion.objects.filter(Pel=idPel)
		
		valoraciones = []
		
		for djv in djVals:
			
			v = valoracion.Valoracion(idUsu=djv.Usu.idUsu, idPel=djv.Pel.idPel, \
													valoracion=djv.puntuacion)
			valoraciones.append(v)
		
		return valoraciones
		
	def actualizaValoracion(self,val):
		""" Actualiza una valoracion anteriormente insertada
		Params:
			val: valoración cuyo rating hay que modificar
		"""
		
		self.inserta(val)
		
	def inserta(self,v):
		"""
		Introduce una valoración, si no existe, se crea, si existe, 
		se actualiza
		
		Params:
		
			v: valoración a insertar
		"""
		
		try:
			
			djv = djModels.Valoracion.objects.get(Pel=v.idPel, Usu=v.idUsu)
			
			djv.puntuacion = v.valoracion
			
		# La valoración no existía y se añade
		except djModels.Valoracion.DoesNotExist:
			
			pel = djModels.Pelicula.objects.get(pk=v.idPel)
			usu = djModels.Usuario.objects.get(pk=v.idUsu)

			djv = djModels.Valoracion(Usu=usu, Pel=pel, puntuacion=v.valoracion)
		
		finally:
			
			djv.save()
	

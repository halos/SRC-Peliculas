#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append('..')

from math import fabs
import valoracion
import motor

class ItemAvgAdj1:
	""" Clase que implementa el método de prediccion
		Item Average Adjustament (All-1) 	
	"""

	def __init__(self):
		""" Constructor básico"""


	def __mediausuario(self, idUsu):
		"""
			Metodo que calcula la media de las valoraciones
			hechas por un usuario a todos sus items
			
			Params:
					idUsu (Integer):
					
			Return:
					media_usuario (Float): Media de las valoraciones hechas por un usuario a todos sus items
			
		"""
		m = motor.Motor() # Clase Singleton
		media_usuario = 0.0
		lval_usuario = m.getValoracionesUsuario(idUsu).values()
		
		for valoracion in lval_usuario:
			media_usuario += valoracion.valoracion
			
		media_usuario /= len(lval_usuario)
		
		return media_usuario

	def __mediaitem(self, idItem):

		"""
			Metodo que calcula la media de las valoraciones
			hechas para un determinado item
			
			Params:
					idItem	(Integer): 
					
			Return:
					media_usuario: Media de las valoraciones hechas para un determinado item
			
		"""
		m = motor.Motor() # Clase Singleton
		media_item = 0.0
		lval_item = m.getValoracionesItem(idItem).values()
		
		for valoracion in lval_item:
			media_item += valoracion.valoracion
		
		media_item /= len(lval_item)
		
		return media_item


	def predice(self, idUsu, idItem, kval_vec):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
				idUsu	(Integer):
				idItem	(Integer): Identificador del item cuyo valora deseamos predecir

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
		m = motor.Motor()
		sum_num = 0.0
		sum_den = 0.0
		media_item = self.__mediaitem(idItem)
		media_usu = self.__mediausuario(idUsu)
		dsim = m.getSimilitudesItem(idItem) # Diccionario de similitudes, clave idItem
		
		#Cálculo de la fórmula de la prediccion		
		for val in kval_vec:
			if val.idPel in dsim:
				simil = dsim.get(val.idPel)
				sum_num += simil.similitud * (val.valoracion - media_usu)
				sum_den += fabs(simil.similitud)	
		
		if sum_den == 0:
			sum_den = 0.00000000001		
		
		vprediccion = sum_num / sum_den + media_item
		prediccion = valoracion.Valoracion(idUsu, idItem, vprediccion)
		
		return prediccion 

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

from math import fabs
from valoracion import Valoracion

class ItemAvgAdj1:
	""" Clase que implementa el método de prediccion
		Item Average Adjustament (All-1) 
		¡No se tiene en cuenta la valoración del item a predecir!	
	"""
	
	def __init__(self, motor):
		""" Constructor básico"""
		self.__motor = motor


	def __mediausuario(self, idUsu, idItem):
		"""
			Metodo que calcula la media de las valoraciones
			hechas por un usuario a todos sus items
			
			Params:
					idUsu (Integer):
					idItem (Integer):
					
			Return:
					media_usuario (Float): Media de las valoraciones hechas por un usuario a todos sus items
			
		"""
		
		lval_usuario = self.__motor.getValoracionesUsuario(idUsu)
		nval = 0
		media_usuario = 0
		for valoracion in lval_usuario:
			if valoracion.idPel != idItem: #Obviamos la valoracion del item a predecir
				media_usuario += valoracion.valoracion
				nval+= 1
		media_usuario /= nval
		return media_usuario

	def __mediaitem(self, idUsu, idItem):

		"""
			Metodo que calcula la media de las valoraciones
			hechas para un determinado item
			
			Params:
					idUsu	(Integer):
					idItem	(Integer): 
					
			Return:
					media_usuario: Media de las valoraciones hechas para un determinado item
			
		"""
		lval_item = self.__motor.getValoracionesItem(idItem)
		nval = 0
		media_item = 0
		for valoracion in lval_item:
			if valoracion.idUsu != idUsu: #Obviamos la valoracion del usuario-item a predecir
				media_item += valoracion.valoracion
				nval+= 1
		media_item /= nval
		return media_item
		
		
	def predice(self, idUsu, idItem):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
				idUsu	(Integer):
				idItem	(Integer): Identificador del item cuyo valora deseamos predecir

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
		
		media_item = self.__mediaitem(idItem)
		media_usu = self.__mediausuario(idUsu)
		sum_num = 0
		sum_den = 0
		lsim = self.__motor.getSimilitudesItem(idItem)
		lval = self.__motor.getValoracionesItem(idUsu)
		#Cálculo de la fórmula de la prediccion		
		if len(lsim) != len(lval):
			print 'Error!'
		for i in len(lsim):
			if lval[i].idPel != idItem: # Obviamos la casilla del item a predecir
				sum_num += lsim[i].similitud * (lval[i].valoracion - media_usu)
				sum_den += fabs(lsim[i].similitud)				
		vprediccion = sum_num / sum_den + media_item
		prediccion = Valoracion(idUsu, idItem, vprediccion)
		return prediccion


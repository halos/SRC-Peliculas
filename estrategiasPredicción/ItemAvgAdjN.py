#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

from math import fabs

class ItemAvgAdjN:
    
	""" Clase que implementa el método de prediccion Item Average Adjustament (N) """

	def __init__(self, idUsu):
		""" Constructor
		
		Params: 
			
			idUsu: Identificador del usuario registrado en el sistema

		"""
		self.idUsu = idUsu


	def mediausuario(self, valoraciones):
		"""
			Metodo que calcula la media de las valoraciones hechas por un usuario a todos sus items
			
			Params:
					
					valoraciones(dict): Valoraciones hechas por todos los usuarios para todos los items
					
			Return:
					media_usuario: Media de las valoraciones hechas por un usuario a todos sus items
			
		"""
			
		lval_usuario = valoraciones.get(self.idUsu)
		nval = 0
		media_usuario = 0
		
		for valoracion in lval_usuario:
		    media_usuario += valoracion.valoracion
		    nval+= 1
		
		media_usuario = media_usuario / nval
		return media_usuario
			    
	def mediaitem(self, idItem, valoraciones):

		"""
			Metodo que calcula la media de las valoraciones hechas para un determinado item
			Params:
					
					valoraciones(dict): Valoraciones hechas por todos los usuarios para todos los items
					
			Return:
					media_usuario: Media de las valoraciones hechas para un determinado item
			
		"""
		media_item = 0
		nval = 0
		
		for lval_usuario in valoraciones.values():
		if idItem in lval_usuario:
			media_item += item.valoracion
			nval += 1
		
		media_item = media_item / nval
		return media_item
			
	def predice(self, idItem, similitudes, valoraciones):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idItem: Identificador del item cuyo valora deseamos predecir
				valoraciones(dict): Contiene todos las valoraciones aportadas por todos los usuarios
				similitudes(dict): Contiene todos los pares de similitud entre items del sistema		
				
		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
		
		media_item = mediaitem(valoraciones)
		media_usuario = mediausuario(valoraciones)
		suma_denom = 0
		suma_num = 0
		
		"Cálculo de la fórmula de la prediccion"
		
		lsimilares = similitudes.get(idItem).values()
		lvaloraciones = valoraciones.get(self.idUsu).values()
		
		for similitud in lsimilares:
			dItem2 = similitud.getIdsPels().get(similitud.getIdsPels().index(idItem) - 1)
			if idItem2 in lvaloraciones:
				suma_denom += math.fabs(similitud.similitud)
				valoracion = lvaloraciones.get(idItem2)
				suma_num += similitud.similitud * (valoracion.valoracion - media_usuario)
			
			vprediccion = suma_num / suma_denom + media_item
			
			return Valoracion(self.idUsu, idItem, vprediccion)


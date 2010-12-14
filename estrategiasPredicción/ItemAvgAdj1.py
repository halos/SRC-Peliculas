#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append("..")

from math import fabs
from valoracion import Valoracion

class ItemAvgAdj1:
	""" Clase que implementa el método de prediccion Item Average Adjustament (All-1) """
	
	def __init__(self):
		""" Constructor básico"""


	def mediausuario(self, idUsu, valoraciones):
		"""
			Metodo que calcula la media de las valoraciones hechas por un usuario a todos sus items
			
			Params:
					
					valoraciones(dict): Valoraciones hechas por todos los usuarios para todos los items
					
			Return:
					media_usuario: Media de las valoraciones hechas por un usuario a todos sus items
			
		"""
			
		lval_usuario = valoraciones.get(idUsu)
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
			if idItem in lval_usuario.keys():
				media_item += lval_usuario.get(idItem).valoracion
				nval += 1
		media_item = media_item / nval
		return media_item
		
		
	def predice(self, idUsu, idItem, similitudes, valoraciones):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idItem: Identificador del item cuyo valora deseamos predecir
				valoraciones(dict): Contiene todos las valoraciones aportadas por todos los usuarios
				similitudes(dict): Contiene los pares de similitud entre items devueltos por el agrupamiento			

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
		
		media_item = self.mediaitem(idItem,valoraciones)
		media_usuario = self.mediausuario(idUsu,valoraciones)
		suma_denom = 0
		suma_num = 0
		
		"Cálculo de la fórmula de la prediccion"
		
		dsimilares = similitudes.get(idItem)
		dvaloraciones = valoraciones.get(idUsu)
		
		for similitud in dsimilares:
			idItem2 = similitud.getIdsPels().get(similitud.getIdsPels().index(idItem) - 1)
			if idItem2 in dvaloraciones.keys():
				suma_denom += fabs(similitud.similitud)
				valoracion = dvaloraciones.get(idItem2)
				suma_num += similitud.similitud * (valoracion.valoracion - media_usuario)
				
		vprediccion = suma_num / suma_denom + media_item
		prediccion = Valoracion(idUsu, idItem, vprediccion)
		return prediccion


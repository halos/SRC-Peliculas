#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

import sys
sys.path.append("..")

from valoracion import Valoracion

class WeithedSum:
    
	""" Clase que implementa el método de prediccion WeithedSum """

	def __init__(self, idUsu):
		""" Constructor básico"""
		self.idUsu = idUsu

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
		suma_denom = 0
		suma_num = 0
		
		"Cálculo de la fórmula de la prediccion"
		
		dsimilares = similitudes.get(idItem)
		dvaloraciones = valoraciones.get(idUsu)
		
		for similitud in dsimilares:
			idItem2 = similitud.getIdsPels().get(similitud.getIdsPels().index(idItem) - 1)
			if idItem2 in dvaloraciones.keys():
				suma_denom += similitud.similitud
				valoracion = dvaloraciones.get(idItem2)
				suma_num += similitud.similitud * valoracion.valoracion
				
		vprediccion = suma_num / suma_denom
		prediccion = Valoracion(idUsu, idItem, vprediccion)
		return prediccion
		



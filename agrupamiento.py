#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"


class Agrupamiento:

	""" Clase que implementa el agrupamiento basado en k-nn """

	def __init__(self, idUsu):
		""" Constructor
	
			Params:
	
			idUsu: Identificador del usuario registrado en el sistema 
			
		"""
		
		self.idUsu = idUsu

	def cmpsimilitud(self, x, y):
		""" Función comparación entre parSimilitud (Clase)
	
			Params:
	
			x: Primer elemento a comparar			
			y: Segundo elemento a comparar
 			
		"""

		return x.similitud - y.similitud
		
	def agrupknn(self, idItem, k, similitudes, valoraciones):
	
		""" Funcion que implementa el algoritmo de agrupamiento k-nn
	
			Params: 
			
			idItem: Identificador del item sobre el que agrupar
			k: nº de elementos similiares a idItem que devolvera el metodo
			similitudes(dict): contiene la tabla de similitud entre items del sistema
			valoraciones(dict): contiene la tabla de valoraciones user-item del sistema
			
			Return:
				
			lksimil(list): contiene <=k paresSimilitud similares a idItem

		"""

		lksimil = similitudes.get(idItem).values()

		"Ordenamos de mayor a menor, segun similitud"
		lksimil.sort(cmp=cmpsimilitud, key=None, reverse=true)

		while i < k | i < lksimil.len():
			pelicula = lksimil[i]
			if pelicula.idPel not in valoraciones.get(self.idUsu):
				similares.append(pelicula)
			i += 1;
			
		return lksimil
            

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"

class Agrupamiento:

	""" Clase que implementa el agrupamiento basado en k-nn """

	def __init__(self):
		""" Constructor
	
			Params:
	
			None
			
		"""
		pass

		
	def agrupknn(self, simItem, valUsu, idItem, k):
	
		""" Funcion que implementa el algoritmo de agrupamiento k-nn
	
			Params: 
			
			None
			
			Return:
				
			vecinos(list): contiene <=k valoraciones elementos vecinos a idItem

		"""
		
		#Agrupamos como posibles vecinos aquellos que estén valorados por el usuario (idUsu)
		vecinos = []		
		for sim in simItem.values():
			if sim.idP1 == idItem:
				idPel = sim.idP2
			else:
				idPel = sim.idP1
			if idPel in valUsu:
				vecinos.append(valUsu.get(idPel))
				
		#Ordenamos de mayor a menor, segun similitud
		vecinos.sort(reverse=True)
		
		# Y devolvemos los k primeros
		return vecinos[:k]
			


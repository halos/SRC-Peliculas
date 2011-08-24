#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"

import motor

class Agrupamiento:

	""" Clase que implementa el agrupamiento basado en k-nn """

	def __init__(self, idUsu):
		""" Constructor
	
			Params:
	
			idUsu: Identificador del usuario registrado en el sistema 
			
		"""
		
		self.__idUsu = idUsu

		
	def agrupknn(self, idItem, k):
	
		""" Funcion que implementa el algoritmo de agrupamiento k-nn
	
			Params: 
			
			idItem: Identificador del item sobre el que agrupar
			k: numero de elementos similiares a idItem que devolvera el metodo
			
			Return:
				
			vecinos(list): contiene <=k valoraciones elementos vecinos a idItem

		"""
		m = motor.Motor()
		lsimil = m.getSimilitudesItem(idItem).values()
		dval_usu = m.getValoracionesUsuario(self.__idUsu)
		#Ordenamos de mayor a menor, segun similitud
		lsimil.sort(reverse=True)
		#Calculamos los k-vecinos al ítem
		i = 0
		vecinos = []
		while i < k | i < lsimil.len():
			if lsimil[i].idP1 == idItem:
				idPel = lsimil[i].idP2
			else:
				idPel = lsimil[i].idP1
			val = dval_usu.get(idPel, 0)
			if val != 0:
				vecinos.append(val)
				i += 1;
		return vecinos

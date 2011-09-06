#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"

import motor
import metricas #Eliminar luego

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
		#Agrupamos como posibles vecinos aquellos que estén valorados por el usuario (idUsu)
		vecinos = []		
		for sim in lsimil:
			if sim.idP1 == idItem:
				idPel = sim.idP2
			else:
				idPel = sim.idP1
			if idPel in dval_usu:
				vecinos.append(dval_usu.get(idPel))
		#Ordenamos de mayor a menor, segun similitud
		vecinos.sort(reverse=True)
		# Y devovemos los k primeros
		return vecinos[:k]

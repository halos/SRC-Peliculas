#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"


class EstrategiaPrediccion:
	""" Interfaz de la estrategia de predicción """
	
	def __init__(self,  pred_func):
		""" Constructor
	
		Params:
	
			pred_func(): Función de predicción
		"""

		self.predice = pred_func

	def predice(self, idItem, lvaloraciones, lsimilitudes):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idItem: Identificador del item cuyo valora deseamos predecir
				lvaloraciones(list): Contiene todos las valoraciones aportadas por todos los usuarios
				lsimilitudes(list): Contiene todos los pares de similitud entre items del sistema			

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
			
		dvaloraciones = {}
			
		for valoracion in lvaloraciones:
			idUsu = valoracion.idUsu
			idItem = valoracion.idPel
			if idUsu not in dvaloraciones:
				dvaloraciones[idUsu] = {}
			dvaloraciones[idUsu, idItem] = valoracion.valoracion
		
		dsimilitudes = {}
			
		for similitud in lsimilitudes:
			idItem1 = similitud.idP1
			idItem2 = similitud.idP2
			if idItem1 not in dvaloraciones:
				dsimilitudes[idItem1] = {}
			dsimilitudes[idItem1, idItem2] = similitud.similitud
			
		prediccion = self.predice(self, idItem, dvaloraciones, dsimilitudes)
				
		return prediccion
			
		
			
            
#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:25:53$"


class EstrategiaPrediccion:
	""" Interfaz de la estrategia de predicción """
	
	def __init__(self, pred_func):
		""" Constructor
	
		Params:
	
			pred_func(): Función de predicción
		"""
		self.predice = pred_func

	def predice(self, idUsu, idItem):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idUsu: Identificador del usuario al que queremos predecir
				idItem: Identificador del item cuyo valor deseamos predecir

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""

		prediccion = self.predice(idUsu, idItem)
		return prediccion
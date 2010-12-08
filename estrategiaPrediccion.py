#!/usr/bin/python
# -*- coding: utf-8 -*-


class EstrategisPrediccion:
	""" Interfaz de la estrategia de predicción """
	
	def __init__(self,  pred_func):
		""" Constructor
	
		Params:
	
			pred_func(): Función de predicción
		"""
		
		self.predice = pred_func

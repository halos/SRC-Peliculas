#!/usr/bin/python
# -*- coding: utf-8 -*-


class Coseno:
	""" Clase que codifica el cálculo de la similitud del coseno """
	
	def __init__ (self):
		""" Constructor """
		pass	
	
	def calcula_similitud(self, u1, u2):
		""" Función que calcula la similitud entre dos usuarios
	
		Params:
	
			u1 (dict): dict{idPel:valoracion}
			u2 (list): dict{idPel:valoracion}
	
		Return:
	
			(float): Similitud entre dos usuarios (0,1)
		"""
		
		

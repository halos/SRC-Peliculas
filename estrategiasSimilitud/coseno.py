#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt

class Coseno:
	""" Clase que codifica el cálculo de la similitud del coseno """
	
	def __init__ (self):
		""" Constructor """
		pass	
	
	def calcula_similitud(self, p1, p2):
		""" Función que calcula la similitud entre dos películas
	
		Params:
	
			p1 (dict): dict{idUsu:valoracion}
			p2 (dict): dict{idUsu:valoracion}
	
		Return:
	
			(float): Similitud entre dos películas (0,1)
		"""
		
		# obtener la lista de todos los usuarios que han valorado la película
		usus = []
		
		for i in p1.keys():
			if i not in usus:
				usus += i
				
		for i in p2.keys():
			if i not in usus:
				usus += i
		
		# Los usuarios que no la hayan visto tenfrán la valoración a 0
		for i in usus:
			if i not in p1.keys():
				p1[i] = 0
			if i not in p2.keys():
				p2[i] = 0
		
		# numerador
		num = 0
		
		for i in usus:
			num += p1[i] * p2[i]
			
		#denominador
		sum1 = 0
		sum2 = 0
		
		for i in usus:
			sum1 += p1[i]**2
			sum2 += p2[i]**2
			
		sum1 = sqrt(sum1)
		sum2 = sqrt(sum2)
		
		den = sum1 * sum2
		
		sim = num / den
		
		return sim

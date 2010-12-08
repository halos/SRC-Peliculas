#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt

class Pearson:
	""" Clase que codifica el cálculo del Coeficiente de Correlación de 
	Pearson """
	
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
		
		# obtener la lista de todas las películas vistas por los dos usuarios
		pels = []
		
		for i in u1.keys():
			if i not in pels:
				pels += i
				
		for i in u2.keys():
			if i not in pels:
				pels += i
		
		# Las películas no valoradas se pondrán a 0
		for i in pels:
			if i not in u1.keys()
				u1[i] = 0
			if i not in u2.keys()
				u2[i] = 0
		
		#medias
		mu1 = float(sum(u1.values()))
		mu1 /= len(u1)
		
		mu2 = float(sum(u2.values()))
		mu2 /= len(u2)
		
		# numerador
		num = 0
		
		for j in pels:
			num += (u1[j] - mu1)(u2[j] - mu2)
		
		# denominador
		sum1 = 0
		sum2 = 0
		
		for j in pels:
			sum1 += (u1[j] - mu1)**2
			sum2 += (u2[j] - mu2)**2
		
		den = sqrt(sum1 * sum2)
		
		sim = num / den
		
		#normaliza similitud
		sim = (sim+1)/2

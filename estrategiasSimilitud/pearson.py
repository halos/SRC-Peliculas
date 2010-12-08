#!/usr/bin/python
# -*- coding: utf-8 -*-

import parSimilitud

class Pearson:
	""" Clase que codifica el cálculo del Coeficiente de Correlación de 
	Pearson """
	
	def __init__ (self):
		""" Constructor """
		pass	
	
	def calcula_parSimilitud(self, u1, u2):
		""" Función que calcula la similitud entre dos usuarios
	
		Params:
	
			u1 (dict): dict{idPel:valoracion}
			u2 (list): dict{idPel:valoracion}
	
		Return:
	
			(ParSimilitud): Similitud entre dos usuarios (0,1)
		"""
		
		# obtener la lista de todas las películas vistas por los dos usuarios
		pels = []
		
		for i in u1.keys():
			if i not in pels:
				pels += i
				
		for i in u2.keys():
			if i not in pels:
				pels += i
		
		#medias
		mu1 = float(sum(u1.values()))
		mu1 /= len(u1)
		
		mu2 = float(sum(u2.values()))
		mu2 /= len(u2)
		
		# numerador
		num = 0
		
		for j in pels:
			
		
		den = 0# denominador
		
		#normaliza similitud
		sim = (sim+1)/2
		

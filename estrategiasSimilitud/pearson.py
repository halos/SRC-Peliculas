#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt
	
def calcula_similitud(_p1, _p2):
	""" Función que calcula la similitud entre dos películas

	Params:

		_p1 (dict): dict{idUsu:valoracion}
		_p2 (dict): dict{idUsu:valoracion}

	Return:

		(float): Similitud entre dos películas (0,1)
	"""
	
	## obtener la lista de todos los usuarios que han valorado la película
	#usus = []
	
	#for i in p1.keys():
		#if i not in usus:
			#usus.append(i)
			
	#for i in p2.keys():
		#if i not in usus:
			#usus.append(i)
	
	## Los usuarios que no la hayan visto tendrán la valoración a 0
	#for i in usus:
		#if i not in p1.keys():
			#p1[i] = 0
		#if i not in p2.keys():
			#p2[i] = 0
	
	#medias
	
	
	mp1 = (float)(sum(_p1.values()))
	mp1 /= len(_p1)
	
	mp2 = (float)(sum(_p2.values()))
	mp2 /= len(_p2)
	
	# numerador
	num = 0
	
	# denominador
	sum1 = 0
	sum2 = 0
	
	for i in _p1:
		if i in _p2:
			# numerador
			num += (_p1[i] - mp1) * (_p2[i] - mp2)
		
			# denominador
			sum1 += (_p1[i] - mp1) ** 2
			sum2 += (_p2[i] - mp2) ** 2
	
	den = sqrt(sum1 * sum2)
	
	if den == 0:
		den = 0.00000000001
	
	sim = num / den	
	
	#normaliza similitud
	sim = (sim + 1) / 2

	return sim

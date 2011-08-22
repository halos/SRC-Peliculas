#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$13-dic-2010 22:18:13$"

import random

class Particionamiento:
	
	""" Clase que implementa el particionamiento de los datos en dos grupos: train y test """

	def __init__(self):
		""" Constructor Básico """

	def divTrainTest(self, valoraciones, pct_train):
		""" Función principal de la clase que divide todas las valoraciones en dos grupos: train y test
		 
    		Params:
    				 
    			valoraciones(list): Lista con todas las valoraciones de todos los usuarios 
    			pct_train: Porcentaje en unidades enteras, que indica la proporcion del conjunto train
    			
    		Return:
    		
    			grupos(tuple): Tupla formada por dos listas de valoraciones (train y test)
				
		"""
		
		nejtrain = len(valoraciones) * ((float)(pct_train) / 100)
		copiav = valoraciones[:]
		train = []
		test = []
		# Repartimos instancias de valoraciones entre train, test según los porcentajes
		for i in range(nejtrain):
			p = random.randint(0,len(copiav) - 1)
			train.append(copiav.pop(p))
		test = copiav[:]
		return (train,test)
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
__author__="sramirez"
__date__ ="$13-dic-2010 22:18:13$"
 
import random
  
class Particionamiento:
	 
	""" Clase que implementa el particionamiento de los datos en dos grupos: train y test """
	 
	def __init__(self, idUsu):
		""" Constructor
		 
		Params:
		 
		idUsu: Identificador del usuario registrado en el sistema 
		 
		"""
		 
		self.idUsu = idUsu
		 
	def divTrainTest(self, valoraciones, pct_train):
		""" Función principal de la clase que divide todas las valoraciones en dos grupos: train y test
		 
		Params:
				 
			valoraciones(list): Lista con todas las valoraciones de todos los usuarios 
			pct_train: Porcentaje en unidades enteras, que indica la proporcion del conjunto train
			
		Return:
		
			grupos(tuple): Tupla formada por dos listas de valoraciones (train y test)
				
		"""
		
		ntrain = valoraciones.len() * (pct_train / 100)
		copiav = valoraciones[:]
		train = []
		test = []
		
		for i in range(ntrain):
			pos = random.randint(0,copiav.len())
			train.append(copiav.pop(pos))
		
		test = copiav[:]
		
		return (train,test)
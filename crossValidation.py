#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$13-dic-2010 22:18:13$"

import sys
sys.path.append("DAO")

import daoValoracion
import daoParSimilitud
import random

class CrossValidation:
	
	""" Clase que implementa el k-fold cross validation, aplicado al espacio del sistema """

	def __init__(self, k):
		""" Constructor Básico """
		self.k = k
		
	def ejecutar(self):
		# Cargamos el fichero de Valoraciones para particionar
		valoraciones = daov.cargarFicheroPrueba("/home/rebellion/Dropbox/Prácticas/Sistemas Informáticos/ratings1.csv")
		# Particionamos el espacio en k-folds
		folds = []
		sizef = (float) (len(valoraciones) / self.k)
		for i in range(self.k):
			folds[i] = []
			for j in range(sizef):
				pos = random.randint(0, len(valoraciones) - 1)
				folds[i].append(valoraciones.pop(pos))
				if not valoraciones: # está vacía
					break
		# Borramos el contenido de las tablas similitudes y valoraciones
		daov = daoValoracion.DAOValoracion()
		daops = daoParSimilitud.DAOParSimilitud()
		daov.reset()
		daops.reset()
		
		
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

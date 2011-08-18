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
		# Cargamos el fichero de Valoraciones para particionar
		valoraciones = daoValoracion.DAOValoracion.cargarFicheroPrueba("/home/rebellion/Dropbox/Prácticas/Sistemas Informáticos/ratings1.csv")
		# Particionamos el espacio en k-folds
		self.folds = []
		sizef = (float) (len(valoraciones) / self.k)
		for i in range(self.k):
			self.folds[i] = []
			for j in range(sizef):
				pos = random.randint(0, len(valoraciones) - 1)
				self.folds[i].append(valoraciones.pop(pos))
				if not valoraciones: # está vacía
					break
		
	def ejecutaIter(self, nfold_test):
		# Utilizar -1 !!
		if nfold_test > self.k | self.k < 0:
			print 'Error!'
		# Borramos el contenido de las tablas similitudes y valoraciones
		daov = daoValoracion.DAOValoracion()
		daops = daoParSimilitud.DAOParSimilitud()
		daov.reset()
		daops.reset()
		# Añadimos al espacio (BD) los folds destinados al entrenamiento
		for i in range(self.k):
			if i != nfold_test - 1: # Sino es el fold de validación, se añade
				lval = self.folds[i]
				for val in lval: # Añadimos cada valoracion del fold
					daov.inserta(val)
		# Devolvemos el fold de validacion
		return self.folds[nfold_test-1]
		
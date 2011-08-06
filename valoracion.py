#!/usr/bin/python
# -*- coding: utf-8 -*-


class Valoracion:
	""" Class doc """
	
	"""id del ususario"""
	idUsu = 0
	
	"""id de la película"""
	idPel = 0
	
	"""valoración"""
	valoracion = 0
	
	def __init__ (self, idUsu, idPel, valoracion):
		""" Class initialiser """
		
		self.idUsu = idUsu
		self.idPel = idPel
		self.valoracion = valoracion
		
	def __cmp__(self, other):
		""" Class compare """
		if self.valoracion < other.valoracion:
			return -1
		elif self.valoracion > other.valoracion:
			return 1
		else:
			return 0		
		
	def setvaloracion(self, valor):
		""" Setter para el atributo valoracion de la pelicula
		
		    Params: 
			
			valor: Nueva valoracion para el par Usuario-Pelicula
		"""
		
		self.valoracion = valor
		
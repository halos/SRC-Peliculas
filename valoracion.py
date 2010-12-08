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
		

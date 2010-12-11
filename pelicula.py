#!/usr/bin/python
# -*- coding: utf-8 -*-

class Pelicula:
	""" Class Pelicula """
	
	"""id de la película"""
	idPel = 0
	
	"""titulo de la pelicula"""
	
	titulo = ""
	
	"""anio de publicacion de la pelicula"""
	
	anio = 0
	
	def __init__ (self, idPel, titulo, anio):
		""" Class initialiser """
		self.idPel = idPel
		self.titulo = titulo
		self.anio = anio

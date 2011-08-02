#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParSimilitud:
	""" Class doc """
	
	"""id de la primera película"""
	idP1 = 0
	
	"""id de la segunda película"""
	idP2 = 0
	
	"""índice de similitud"""
	similitud = 0.0
	
	def __init__ (self, idP1, idP2, similitud):
		""" Calse qeu codifica una similitud entre dos películas """
		
		self.idP1 = idP1
		self.idP2 = idP2
		self.similitud = similitud
		
	def __eq__(self, other):
		""" == : Comapra si los usuarios son los mismos
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud se refieren al
			mismo usuario.
		"""
		
		return (self.idP1,self.idP2) == (other.idP1,other.idP2) | \
		(self.idP1,self.idP2) == (other.idP2,other.idP1)

	def __ne__(self, other):
		""" == : Comapra si los usuarios son diferentes
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud no se refieren
			al mismo usuario.
		"""
		
		return (self.idP1,self.idP2) != (other.idP1,other.idP2) & \
		(self.idP1,self.idP2) != (other.idP2,other.idP1)
		
	def setsimilitud(self, similitud):
		""" Setter para el atributo similitud
		
		    Params: 
			
			similitud: nuevo valor de similitud para el par Pelicula-Pelicula
		
		"""
		
		self.similitud = similitud

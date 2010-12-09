#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParSimilitud:
	""" Clase que codifica la similitud entre dos usuarios """
	
	"""id de la primera película"""
	idP1 = 0
	
	"""id de la segunda película"""
	idP2 = 0
	
	"""índice de similitud"""
	similitud = 0.0
	
	def __init__ (self, idP1, idP2, similitud):
		""" Clase que codifica una similitud entre dos películas """
		
		self.idP1 = idP1
		self.idP2 = idP2
		self.similitud = similitud
		
	def __eq__(self, other):
		""" == : Compara si las dos películas son las mismas
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud se refieren a
			la misma película.
		"""
		
		return (self.idP1,self.idP2) == (other.idP1,other.idP2) | \
		(self.idP1,self.idP2) == (other.idP2,other.idP1)

	def __ne__(self, other):
		""" == : Comapra si las película son diferentes
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud no se refieren
			a la misma película.
		"""
		
		return ((self.idP1,self.idP2) != (other.idP1,other.idP2)) & ((self.idP1,self.idP2) != (other.idP2,other.idP1))

	def __repr__(self):
		"""Método para obtener una representación en cadena de la clase"""
		
		cad = "%s <==> %s : %f" % (self.idP1, self.idP2, self.similitud)

		return cad

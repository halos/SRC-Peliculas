#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParSimilitud:
	""" Clase que codifica la similitud entre dos usuarios """
	
	"""id del primer usuario"""
	idU1 = 0
	
	"""id del segundo usuario"""
	idU2 = 0
	
	"""índice de similitud"""
	similitud = 0.0
	
	def __init__ (self, idU1, idU2, similitud):
		""" Clase que codifica una similitud entre dos películas """
		
		self.idU1 = idU1
		self.idU2 = idU2
		self.similitud = similitud
		
	def __eq__(self, other):
		""" == : Compara si los usuarios son los mismos
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud se refieren al
			mismo usuario.
		"""
		
		return (self.idU1,self.idU2) == (other.idU1,other.idU2) | \
		(self.idU1,self.idU2) == (other.idU2,other.idU1)

	def __neq__(self, other):
		""" == : Comapra si los usuarios son diferentes
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud no se refieren
			al mismo usuario.
		"""
		
		return (self.idU1,self.idU2) != (other.idU1,other.idU2) & \
		(self.idU1,self.idU2) &= (other.idU2,other.idU1)

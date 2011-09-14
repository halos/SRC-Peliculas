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
		
	def __cmp__(self, other):
		""" Class compare """
		if self.similitud < other.similitud:
			return -1
		elif self.similitud > other.similitud:
			return 1
		else:
			return 0
		
	def __eq__(self, other):
		""" == : Comapra si los usuarios son los mismos
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si los dos ParSimilitud se refieren al
			mismo usuario.
		"""
		
		return (self.idP1,self.idP2) == (other.idP1,other.idP2) or \
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
		
		return (self.idP1,self.idP2) != (other.idP1,other.idP2) and \
		(self.idP1,self.idP2) != (other.idP2,other.idP1)
		
	def setsimilitud(self, similitud):
		""" Setter para el atributo similitud
		
		    Params: 
			
			similitud: nuevo valor de similitud para el par Pelicula-Pelicula
		
		"""
		
		self.similitud = similitud

	def __lt__(self, other):
		""" Operador < para el grado de similitud
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si el objeto es menor que el segundo 
		"""
		
		return self.similitud < other.similitud
		
	def __gt__(self, other):
		""" Operador > para el grado de similitud
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si el objeto es mayor que el segundo 
		"""
		
		return self.similitud > other.similitud

	def __le__(self, other):
		""" Operador <= para el grado de similitud
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si el objeto es menor o igual que el segundo 
		"""
		
		return self.similitud <= other.similitud
		
	def __ge__(self, other):
		""" Operador >= para el grado de similitud
	
		Params:
	
			other(ParSimilitud): El otro ParSimilitud con el que va ser
			comparado
	
		Return:
	
			(bool): Boobleano indicando si el objeto es mayor o igual que el segundo 
		"""
		
		return self.similitud >= other.similitud

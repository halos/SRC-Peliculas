#!/usr/bin/python
# -*- coding: utf-8 -*-

class Motor:
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		self.__daov = DAOValoracion()
		self.__daou = DAOUsuario()
		self.__daop = DAOPelicula()
		self.__daos = DAOParSimilitud()		

	def getValoracionesUsuario(self, idUsu):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		return self.__daov.getValoracionesUsuario(idUsu)
		
		
	def getValoracionesItem(self, idItem):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		return self.__daov.getValoracionesItem(idItem)
		
	def getValoraciones(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		return self.__daov.getValoraciones()
		
	def getSimilitudes(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		return self.__daos.getSimilitudes()
		
	def getSimilitudesItem(self, idItem):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		return self.__daos.getSimilitudesItem(idItem)

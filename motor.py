#!/usr/bin/python
# -*- coding: utf-8 -*-

import estrategiaSimilitud

class Motor:
	""" Class doc """
	
	"""Identificador del usuario actual"""
	__user = 0
	
	"""Número de valoraciones que se lleva sin actualizar el modelo"""
	__nvaloraciones = 0
	
	"""Valoraciones nuevas desde que se actualizó el modelo por última vez"""
	__nuevasValoraciones = []
	
	def __init__ (self):
		""" Class initialiser """
		pass
		
	def login(self, id, passw):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daou = DAOUsuario()
		self.__user = daou.getUsuario(id)
		if self.__comprobarIdentidad(self.__user, passw):
			self.__actualizarModelo()
			return True
		return False
	
	def valorarPelicula(self, idPel, val):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		valoracion = Valoracion(self.__user.idUsu, idPel, val)
		daov = DAOValoracion()
		daov.inserta(valoracion) # Si existe, se actualiza
		__nuevasValoraciones.append(valoracion)
		
		# Cuando el nº de inserciones sea 5, actualizamos el modelo
		self.__nvaloraciones += 1
		if self.__nvaloraciones == 5:
			self.__actualizarModelo()
			self.__nvaloraciones = 0
		
	def buscarPeliculas(self, consulta):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daop = DAOPelicula()
		lpel = daop.getPeliculasTitulo(consulta)
		return lpel
	
	def __comprobarIdentidad(self, user, passw):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		if user.passw == passw:
			return True
		return False
	
	def __actualizarModelo(self): # Para javi
		""" Método para actualizar el modelo tras haber nuevas valoraciones
	
		Params:
	
			None
	
		Return:
	
			None
		"""
		
		valoraciones = []
		
		#obtener valoraciones de todas las películas puntuadas
		for v in __nuevasValoraciones:
			valoraciones += self.getValoracionesItem(v.idPel)
		
		eSimilitud = estrategiaSimilitud.estrategiaSimilitud()
		similitudes = eSimilitud.actualizaSimilitud(valoraciones, __nuevasValoraciones)
		
		#almacenamiento de las similitudes
		

	def recomendar(self):
			""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		# Por implementar (Sergio)
	
	# Métodos adicionales (getter's)

	def getValoracionesUsuario(self, idUsu):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daov = DAOValoracion()
		return daov.getValoracionesUsuario(idUsu)
		
		
	def getValoracionesItem(self, idItem):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daov = DAOValoracion()
		return daov.getValoracionesItem(idItem)
		
	def getValoraciones(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daov = DAOValoracion()
		return daov.getValoraciones()
		
	def getSimilitudes(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daos = DAOParSimilitud()
		return daos.getSimilitudes()
		
	def getSimilitudesItem(self, idItem):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daos = DAOParSimilitud()
		return daos.getSimilitudesItem(idItem)

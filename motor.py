#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('DAO')

from valoracion import Valoracion
from singleton import Singleton
from daoParSimilitud import *
from daoPelicula import *
from daoValoracion import *
from daoUsuario import *
import estrategiaSimilitud
from estrategiaPrediccion import EstrategiaPrediccion

class Motor (Singleton):
	
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
		self.__nuevasValoraciones.append(valoracion)
		
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
		for v in self.__nuevasValoraciones:
			valoraciones += self.getValoracionesItem(v.idPel)
		
		eSimilitud = estrategiaSimilitud.estrategiaSimilitud()
		similitudes = eSimilitud.actualizaSimilitud(valoraciones, self.__nuevasValoraciones)
		
		#almacenamiento de las similitudes
		

	def recomendar(self, func_pred):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daop = DAOPelicula()
		# Añadimos función de predicción 
		ep = EstrategiaPrediccion(func_pred)
		lpelnop = daop.getPeliculasNoPuntuadas(self.__user.idUsu) # devuelve una lista de idPel, de aquellas películas no puntuadas por ese usuario
		# Creamos una lista de valores predichos
		lvalpred = []
		for idPel in lpelnop:
			prediccion = ep.predice(self.__user, idPel)
			val = Valoracion(self.__user, idPel, prediccion)
			lvalpred.append(val)
		# Ordenamos los elementos "Valoraciones", de forma descendente y por el valor de la puntación
		lvalpred.sort(reverse=True)
		return lvalpred[:5]
		
		
		
	
	# Métodos adicionales (getter's)

	def getValoracionesUsuario(self, idUsu):
		""" Método que devuelve el conjunto de las valoraciones hechas por un usuario para todas las películas puntuadas.
	
		Params:
	
			idUsu (Integer): Número de que identifica al usuario en la aplicación 
	
		Return:
	
			Diccionario de valoraciones, cuyas claves son el idItem 
			
		"""
		daov = DAOValoracion()
		return daov.getValoracionesUsuario(idUsu)
		
		
	def getValoracionesItem(self, idItem):
		""" Método que devuelve el conjunto de las valoraciones hechas para una película en concreto, por todos los usuarios del sistema.
	
		Params:
	
			idItem (Integer): Número de que identifica a la película en la aplación
	
		Return:
	
			Diccionario de valoraciones, cuyas claves son el idUsuario
			
		"""
		daov = DAOValoracion()
		return daov.getValoracionesItem(idItem)
		
	def getValoraciones(self):
		""" Método que devuelve el conjunto de todas las valoraciones hechas para todos los usuarios.
	
		Params:
	
			None
	
		Return:
	
			Diccionario de diccionarios, cuyas claves son el idUsu (primero), y despúes el idItem. 
			
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
		""" Método que devuelve el conjunto de las similitudes entre el item seleccionado y el resto.
	
		Params:
	
			idItem (Integer): Número de que identifica a la película en la aplación
	
		Return:
	
			Diccionario de similitudes, cuyas claves son el idItem del elemento a comparar.
			
		"""
		daos = DAOParSimilitud()
		return daos.getSimilitudesItem(idItem)

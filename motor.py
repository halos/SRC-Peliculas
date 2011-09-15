#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('DAO')

import valoracion
import singleton
import daoValoracion
import daoUsuario
import daoPelicula
import daoParSimilitud
import estrategiaSimilitud
import estrategiaPrediccion

class Motor (singleton.Singleton):
	
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
		daou = daoUsuario.DAOUsuario()
		self.__user = daou.getUsuario(id)
		if self.__comprobarIdentidad(self.__user, passw):
			self.actualizarModelo()
			return True
		return False
	
	def valorarPelicula(self, idPel, val):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		val_nueva = valoracion.Valoracion(self.__user.idUsu, idPel, val)
		daov = daoValoracion.DAOValoracion()
		daov.inserta(val_nueva) # Si existe, se actualiza
		self.__nuevasValoraciones.append(val_nueva)
		
		# Cuando el nº de inserciones sea 5, actualizamos el modelo
		self.__nvaloraciones += 1
		if self.__nvaloraciones == 5:
			self.actualizarModelo()
			self.__nvaloraciones = 0
		
	def buscarPeliculas(self, consulta):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daop = daoPelicula.DAOPelicula()
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
	
	def crearModelo(self, estrat_sim):
		""" Método para crear el modelo desde cero, borrando similitudes anteriores
			Params:
			
				None
			
			Return:
		
				None		
		"""		
		# Obtenemos todas las valoraciones de la BD
		valoraciones = self.getValoraciones()
		
		estrat_sim.insertaSimilitud(valoraciones)

	def recomendar(self, estra_pred):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		daop = daoPelicula.DAOPelicula()		
		lpelnop = daop.getPeliculasNoPuntuadas(self.__user.idUsu) # devuelve una lista de idPel, de aquellas películas no puntuadas por ese usuario
		# Creamos una lista de valores predichos
		lvalpred = []
		for idPel in lpelnop:
			prediccion = estra_pred.predice(self.__user, idPel)
			val = valoracion.Valoracion(self.__user, idPel, prediccion)
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
		
		return daoValoracion.DAOValoracion().getValoracionesUsuario(idUsu)
		
		
	def getValoracionesItem(self, idItem):
		""" Método que devuelve el conjunto de las valoraciones hechas para una película en concreto, por todos los usuarios del sistema.
	
		Params:
	
			idItem (Integer): Número de que identifica a la película en la aplación
	
		Return:
	
			Diccionario de valoraciones, cuyas claves son el idUsuario
			
		"""
		
		return daoValoracion.DAOValoracion().getValoracionesItem(idItem)
		
	def getValoraciones(self):
		""" Método que devuelve el conjunto de todas las valoraciones hechas
		para todos los usuarios.
	
		Params:
	
			None
	
		Return:
	
			(list): Lista de objetos Valoracion
			
		"""
		
		return daoValoracion.DAOValoracion().getValoraciones()
		
	def getSimilitudes(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		
		return daoParSimilitud.DAOParSimilitud().getSimilitudes()
		
	def getSimilitudesItem(self, idItem):
		""" Método que devuelve el conjunto de las similitudes entre el item seleccionado y el resto.
	
		Params:
	
			idItem (Integer): Número de que identifica a la película en la aplación
	
		Return:
	
			Diccionario de similitudes, cuyas claves son el idItem del elemento a comparar.
			
		"""
		
		return daoParSimilitud.DAOParSimilitud().getSimilitudesItem(idItem)

	def insertaSimilitudes(self, _similitudes):
		""" Método para insertar nuevas similitudes
	
		Params:
	
			_similitudes(list): Lista de similitudes
	
		Return:
	
			(Nonetype): None
		"""
		
		daoParSimilitud.DAOParSimilitud().insertaSimilitudes(_similitudes)
			
	def borraSimilitudes(self):
		""" Método para borrar todaas las similitudes existentes (Cuidado!)
	
		Params:
	
			None
	
		Return:
	
			(Nonetype): None
		"""
		
		daoParSimilitud.DAOParSimilitud().reset()

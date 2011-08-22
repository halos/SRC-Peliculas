#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import valoracion
import db
import singleton

class DAOValoracion(singleton.Singleton):
	""" Class doc """
	
	def getValoraciones(self):
		"""
		metodo que devuelve todas las valoraciones realizadas
		"""
		
		datos = db.DB()
		res = datos.get_filas("SELECT * FROM valoraciones")
		valoraciones = {}
		for i in res:
			if i[1] not in valoraciones:
				#si el usuario no está en el diccionario
				#se introduce con un diccionario vacío
				valoraciones[i[1]] = {}
			valoraciones[i[1]][i[0]] = \
			valoracion.Valoracion(i[1], i[0], i[2])
		return valoraciones
	
	def __init__ (self):
		""" Class initialisera """
		
		pass

	def inserta(self,v):
		"""
		introduce una nueva valoración a tener en cuenta
		params:
			v: valoración a insertar
		"""
		
		datos= db.DB()
		consulta = "INSERT INTO `valoraciones` (`idPelicula`, `idUsuario`, `valoracion`) VALUES ("+\
		str(v.idPel) + "," + str(v.idUsu) + "," + str(v.valoracion) + ")"
		print consulta
		datos.ejecutar(consulta)
		return
	
	def getValoracionesUsuario(self,idUsu):
		""" obtiene las valoraciones para todas las peliculas de un usuario concreto
		params:
			idUsu: identificador del usuario
		"""
		
		datos = db.DB()
		consulta="SELECT * FROM valoraciones WHERE idUsuario = "+str(idUsu)
		res=datos.get_filas(consulta)
		valoraciones = {}
		
		for i in res:
			valoraciones[i[0]] = valoracion.Valoracion(i[1], i[0], i[2])
		
		return valoraciones
	
	def getValoracionesItem(self,idPel):
		""" obtiene las valoraciones que todos los usuarios han realizado sobre una pelicula concreta
		params:
			idPel: identificador de la pelicula
		"""
		datos = db.DB()
		consulta = "SELECT * FROM valoraciones WHERE idPelicula = "+str(idPel)
		res = datos.get_filas(consulta)
		valoraciones = {}
		
		for i in res:
			valoraciones[i[1]] = valoracion.Valoracion(i[1], i[0], i[2])
		
		return valoraciones
	
	def actualizaValoracion(self,val):
		""" Actualiza una valoracion anteriormente insertada
		Params:
			val: valoración cuyo rating hay que modificar
		"""
		
		datos = db.DB()
		consulta = "UPDATE valoraciones SET valoracion ="+\
		str(val.valoracion) + " WHERE (idPelicula=" + str(val.idPel) + \
		" AND idUsuario=" + str(val.idUsu)+")"
		print consulta
		datos.ejecutar(consulta)
		
		return

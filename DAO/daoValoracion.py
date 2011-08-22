#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
sys.path.append('..')

import valoracion
import db
import singleton

class DAOValoracion(singleton.Singleton):
	""" Class doc """
	
	def getValoraciones(self):
		""" Método que devuelve todas las valoraciones realizadas
	
		Params:
	
			None
	
		Return:
	
			(list): Lista de objetos Valoracion
		"""
		
		datos = db.DB()
		res = datos.get_filas("SELECT * FROM valoraciones")
		valoraciones = []
		
		for r in res:
			
			v = valoracion.Valoracion(idUsu=r[1], idPel=r[0], valoracion=r[2])
			valoraciones.append(v)
		
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
	
	def reset(self):
		"""Elimina todos los datos de la tabla de valoraciones
		
		ADVERTENCIA: usar sólo para pruebas del estudio de casos
		"""
		datos=db.DB()
		consulta = "DELETE FROM valoraciones"
		datos.ejecutar (consulta)
		return
	
	def cargarFicheroPrueba(self,fichero):
		""" lee de un fichero csv un conjunto de valoraciones con las que poder trabajar
		Params:
			fichero: nombre del fichero csv del que se va a leer
		return:
			lista de valoraciones leidas del fichero
		ADVERTENCIA: se espera que los campos del fichero csv estén separados por comas.
		"""
		reader=csv.reader(open(fichero, 'rb'))
		ratings=[]
		for fila, i in enumerate(reader):
			ratings.append(valoracion.Valoracion(i[1],i[0],i[2]))
		return ratings

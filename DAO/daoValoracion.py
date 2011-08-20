#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import sys
sys.path.append('..')

import valoracion
from db import *
from singleton import *

class DAOValoracion(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	
	def getValoraciones(self):
		"""
		metodo que devuelve todas las valoraciones realizadas
		"""
		datos = DB()
		res=datos.get_filas("SELECT * FROM valoraciones")
		valoraciones={}
		for i in res:
			if i[1] not in valoraciones:
				#si el usuario no está en el diccionario
				#se introduce con un diccionario vacío
				valoraciones[i[1]]={}
			valoraciones[i[1]][i[0]]=\
			valoracion.Valoracion(i[1],i[0],i[2])
		return valoraciones

	def insertaValoracion(self, v):
		"""
		Introduce una nueva valoración a tener en cuenta
		params:
			vals: valoracióna insertar
		"""
		datos=DB()
		consulta = "INSERT INTO `valoraciones` (`idPelicula`, `idUsuario`, `valoracion`) VALUES ("+\
		str(v.idPel)+","+str(v.idUsu)+","+str(v.valoracion)+")"
		datos.ejecutar(consulta)

	def insertaValoraciones(self, lval):
		"""
		introduce una nueva valoración a tener en cuenta
		params:
			vals: lista de valoraciones a insertar
		"""
		datos = DB()
		consulta = "INSERT INTO `valoraciones` (`idPelicula`, `idUsuario`, `valoracion`) VALUES "
		for i in range(lval) - 1:
			consulta += "(" + str(lval[i].idPel) + "," + str(lval[i].idUsu) + "," + str(lval[i].valoracion) + "), "
		consulta += "(" + str(lval[-1].idPel) + "," + str(lval[-1].idUsu) + "," + str(lval[-1].valoracion) + ");"
		datos.ejecutar(consulta)
		return
	
	def getValoracionesUsuario(self,idUsu):
		""" obtiene las valoraciones para todas las peliculas de un usuario concreto
		params:
			idUsu: identificador del usuario
		"""
		datos=DB()
		consulta="SELECT * FROM valoraciones WHERE idUsuario = "+str(idUsu)
		res=datos.get_filas(consulta)
		valoraciones={}
		for i in res:
			valoraciones[i[0]]=valoracion.Valoracion(i[1],i[0],i[2])
		return valoraciones
	
	def getValoracionesItem(self,idPel):
		""" obtiene las valoraciones que todos los usuarios han realizado sobre una pelicula concreta
		params:
			idPel: identificador de la pelicula
		"""
		datos=DB()
		consulta="SELECT * FROM valoraciones WHERE idPelicula = "+str(idPel)
		res=datos.get_filas(consulta)
		valoraciones={}
		for i in res:
			valoraciones[i[1]]=valoracion.Valoracion(i[1],i[0],i[2])
		return valoraciones
	
	def actualizaValoracion(self,val):
		""" Actualiza una valoracion anteriormente insertada
		Params:
			val: valoración cuyo rating hay que modificar
		"""
		datos=DB()
		consulta="UPDATE valoraciones SET valoracion ="+\
		str(val.valoracion)+" WHERE (idPelicula="+str(val.idPel)+\
		" AND idUsuario="+str(val.idUsu)+")"
		datos.ejecutar(consulta)
		return
	
	def reset(self):
		"""Elimina todos los datos de la tabla de valoraciones
		
		ADVERTENCIA: usar sólo para pruebas del estudio de casos
		"""
		datos=DB()
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

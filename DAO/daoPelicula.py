#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import pelicula
from db import *
from singleton import *
from daoValoracion import *

class DAOPelicula(Singleton):
	""" Class doc """
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getPeliculas(self):
		"""devuelve todas las peliculas con las que se trabaja"""
		datos = DB()
		res=datos.get_filas("SELECT * FROM peliculas")
		pelis=[]
		for i in res:
			pelis.append(pelicula.Pelicula(i[0],i[2],i[1]))
		return pelis
	
	def getPeliculasTitulo(self,tit):
		"""
		Busca entre todas las peliculas aquellas que coinciden con el titulo proporcionado
		Params:
			tit: titulo de la pelicula a buscar
		"""
		datos=DB()
		consulta= "SELECT * FROM peliculas WHERE titulo like '%"
		consulta += tit
		consulta += "%'"
		res=datos.get_filas(consulta)
		pelis=[]
		for i in res:
			pelis.append(pelicula.Pelicula(i[0],i[2],i[1]))
		return pelis
	
	def getPelicula(self,id):
		"""
		Busca la pelicula que coincide exactamente con el id suministrado
		Params:
			id: id de la película a devolver
		"""
		datos=DB()
		consulta="SELECT * FROM peliculas WHERE id = "+str(id)
		res=datos.get_fila(consulta)
		peli=pelicula.Pelicula(res[0],res[2],res[1])
		return peli
	
	def getPeliculasNoPuntuadas(self,idUsu):
		"""
		Para un usuario concreto devuelve aquellas películas que no han sido valoradas
		Params:
			idUsu: usuario cuyas peliculas no valoradas se van a buscar
		"""
		datos=DB()
		daov=DAOValoracion()
		vals=daov.getValoracionesUsuario(idUsu)
		excluidos=""
		for i in vals:
			excluidos+=str(i.idPel)+","
		#eliminamos la última coma, innecesaria
		excluidos2=excluidos[:-1]
		consulta="SELECT * FROM peliculas WHERE id NOT IN ("+excluidos2+")"
		res=datos.get_filas(consulta)
		pelis=[]
		for j in res:
			pelis.append(pelicula.Pelicula(j[0],j[2],j[1]))
		return pelis
		

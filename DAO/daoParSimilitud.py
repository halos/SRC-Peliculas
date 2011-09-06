#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import parSimilitud
from db import *
from singleton import *

class DAOParSimilitud(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getSimilitudes(self):
		"""
		Obtiene todas las similitudes entre items generadas
		"""
		datos = DB()
		res = datos.get_filas("SELECT * FROM similitudes")
		similitudes = []
		for i in res:
			ps = parSimilitud.ParSimilitud(i[0],i[1],i[2])
			similitudes.append(ps)
		return similitudes
		
	def getSimilitudesItem(self,idItem):
		"""
		Obtiene todas las similitudes que implican un item en concreto
		params:
			idItem: Identificador del item cuyas similitudes se buscan
		"""
		datos = DB()
		# El método se ha implementado así por razones de eficiencia, una consulta OR en el WHERE es ineficiente en BD
		consulta1 = "SELECT * FROM similitudes WHERE idPel1 = " + str(idItem)
		consulta2 = "SELECT * FROM similitudes WHERE idPel2 = " + str(idItem)
		
		res1 = datos.get_filas(consulta1)
		res2 = datos.get_filas(consulta2)
		
		similitudes = {}
		for i in res1:
			if i[0] != idItem:
				similitudes[i[0]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])
			else:
				similitudes[i[1]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])
		for i in res2:
			if i[0] != idItem:
				similitudes[i[0]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])
			else:
				similitudes[i[1]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])
	
		return similitudes

	
	def insertaSimilitud(self,sim):
		"""
		Inserta un nuevo par de similitud
		Params:
			sim: Similitud a insertar
		"""
		datos=DB()
		consulta = "INSERT INTO similitudes (idPel1, idPel2, similitud) VALUES ("+\
		str(sim.idP1)+","+str(sim.idP2)+","+str(sim.similitud)+")"
		datos.ejecutar(consulta)
		return
	
	def insertaSimilitudes(self, lsim):
		"""
		Inserta una lista de pares-similitud
		Params:
			lsim: Lista de pares a insertar
		"""
		consulta = "INSERT INTO similitudes (idPel1, idPel2, similitud) VALUES "
		
		for i in range(len(lsim) - 1): # Obviamos el último elemento
			consulta += "(" + str(lsim[i].idP1) + "," + str(lsim[i].idP2) + "," + str(lsim[i].similitud) + "), "
		consulta += "(" + str(lsim[-1].idP1) + "," + str(lsim[-1].idP2) + "," + str(lsim[-1].similitud) + ");"
		
		datos = DB()
		datos.ejecutar(consulta)
		return
		
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		datos = DB()
		consulta = " UPDATE similitudes SET similitud = " + str(sim.similitud) +\
		" WHERE (idPel1 = " + str(sim.idP1) + " AND idPel2 = " + str(sim.idP2) + ") OR " +\
		" (idPel1 = " + str(sim.idP2) + "AND idPel2 = " + str(sim.idP1) + ")"
		datos.ejecutar(consulta)
		return
	
	def reset(self):
		"""Elimina todos los datos de la tabla de similitudes
		
		ADVERTENCIA: usar sólo para pruebas del estudio de casos
		"""
		datos=DB()
		consulta = "DELETE FROM similitudes"
		datos.ejecutar (consulta)
		return
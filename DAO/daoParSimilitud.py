#!/usr/bin/python
# -*- coding: utf-8 -*-

import parSimilitud
import db
from singleton import *

class DAOParSimilitud(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getSimilitudes(self):
		"""
		Obtiene todas las similitudes entre items generadas
		(CUIDADO!) Método costoso en memoria - millones de tuplas
		"""
		datos = db.DB()
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
		datos = db.DB()
		# El método se ha implementado así por razones de eficiencia, una consulta OR en el WHERE es ineficiente en BD
		consulta = "SELECT * FROM similitudes WHERE idPel1 = " + str(idItem)
		res = datos.get_filas(consulta)
		
		similitudes = {}
		
		for i in res:
			if i[0] != idItem:
				similitudes[i[0]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])
			else:
				similitudes[i[1]] = parSimilitud.ParSimilitud(i[0],i[1],i[2])

	
	def insertaSimilitud(self,sim):
		"""
		Inserta un nuevo par de similitud
		Params:
			sim: Similitud a insertar
		"""
		# Insertamos el parSimilitud doblemente, con el orden de id's alternado
		datos = db.DB()
		consulta = "INSERT INTO similitudes (idPel1, idPel2, similitud) VALUES (" + \
		str(sim.idP1) + "," + str(sim.idP2) + "," + str(sim.similitud) + "), (" + \
		str(sim.idP2) + "," + str(sim.idP1) + ";" + str(sim.similitud) + ")"

		datos.ejecutar(consulta)
		return
	
	def insertaSimilitudes(self, lsim):
		"""
		Inserta una lista de pares-similitud
		Params:
			lsim: Lista de pares a insertar
		"""
		consulta = "INSERT INTO similitudes (idPel1, idPel2, similitud) VALUES "
		
		# Insertamos el parSimilitud doblemente, con el orden de id's alternado
		for i in range(len(lsim) - 1): # Obviamos el último elemento
			consulta += "(" + str(lsim[i].idP1) + "," + str(lsim[i].idP2) + "," + str(lsim[i].similitud) + "), "
			consulta += "(" + str(lsim[i].idP2) + "," + str(lsim[i].idP1) + "," + str(lsim[i].similitud) + "), "
		
		consulta += "(" + str(lsim[-1].idP1) + "," + str(lsim[-1].idP2) + "," + str(lsim[-1].similitud) + "),"
		consulta += "(" + str(lsim[-1].idP2) + "," + str(lsim[-1].idP1) + "," + str(lsim[-1].similitud) + ");"
		
		datos = db.DB()
		datos.ejecutar(consulta)
		return
		
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		datos = db.DB()
		consulta = " UPDATE similitudes SET similitud = " + str(sim.similitud) +\
		" WHERE (idPel1 = " + str(sim.idP1) + " AND idPel2 = " + str(sim.idP2) + ") AND " +\
		" (idPel1 = " + str(sim.idP2) + "AND idPel2 = " + str(sim.idP1) + ")"
		
		datos.ejecutar(consulta)
		return
	
	def reset(self):
		"""Elimina todos los datos de la tabla de similitudes
		
		ADVERTENCIA: usar sólo para pruebas del estudio de casos
		"""
		datos = db.DB()
		consulta = "TRUNCATE similitudes" # Más rapido (también para índices)
		
		datos.ejecutar (consulta)
		return
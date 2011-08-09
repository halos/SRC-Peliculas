#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		res=datos.get_filas("SELECT * FROM similitudes")
		similitudes=[]
		for i in res:
			similitudes.append(parSimilitud.ParSimilitud(i[0],i[1],i[2]))
		return similitudes
		
	def getSimilitudesItem(self,idItem):
		"""
		Obtiene todas las similitudes que implican un item en concreto
		params:
			idItem: Identificador del item cuyas similitudes se buscan
		"""
		datos = DB()
		consulta= "SELECT * FROM similitudes WHERE idPel1 = "+str(idItem)
		res=datos.get_filas(consulta)
		similitudes=[]
		for i in res:
			similitudes.append(parSimilitud.ParSimilitud(i[0],i[1],i[2]))
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
		
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		datos=DB()
		consulta= "UPDATE similitudes SET similitud="+str(sim.similitud)+\
		" WHERE (idPel1="+str(sim.idP1)+" AND idPel2="+str(sim.idP2)+")"
		print consulta
		datos.ejecutar(consulta)
		return
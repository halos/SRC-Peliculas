#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from singleton import *

sys.path.append('..')

import parSimilitud
import srcp.models as djModels

class DAOParSimilitud(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getSimilitudes(self):
		""" Obtiene todas las similitudes entre items generadas
	
		Params:
	
			None
	
		Return:
	
			(dict): {idPel1:{idPel2:parSimilitud}
		"""
		
		djSimilitudes = djModels.Similitud.objects.all()
		
		similitudes = {}
		
		for djs in djSimilitudes:
			
			if djs.idPel1 not in similitudes:
				#si el item1 no está en el diccionario
				#se introduce con un diccionario vacío
				similitudes[djs.idPel1] = {}
				
			if djs.idPel2 not in similitudes:
				#si el item1 no está en el diccionario
				#se introduce con un diccionario vacío
				similitudes[djs.idPel2] = {}

			
			ps = parSimilitud.ParSimilitud(djs.idPel1, djs.idPel2, djs.valoracion)
			
			similitudes[djs.idPel1][djs.idPel2] = ps
			similitudes[djs.idPel2][djs.idPel1] = ps
			
		return similitudes
		
	def getSimilitudesItem(self,idPel):
		""" Obtiene todas las similitudes que implican un item en concreto
	
		Params:
	
			idPel(int): Identificador del item cuyas similitudes se buscan
	
		Return:
	
			(dict): {idPel:parSimilitud}
		"""
		
		djSimilitudes = []
		djSimilitudes += djModels.Similitud.objects.filter(idPel1=idPel)
		djSimilitudes += djModels.Similitud.objects.filter(idPel2=idPel)

		similitudes={}
		
		for djs in djSimilitudes:
			
			ps = parSimilitud.ParSimilitud(djs.idPel1, djs.idPel2, djs.valoracion)
		
			if s.idPel1 != idPel:
				similitudes[s.idPel1] = ps
		
			else:
				similitudes[s.idPel2] = ps

		return similitudes

	
	def insertaSimilitud(self,sim):
		"""
		Inserta un nuevo par de similitud
		Params:
			sim: Similitud a insertar
		"""
		djs = djModels.Similitud(idPel1=sim.idP1, idPel2=sim.idP2, \
													valoracion=sim.similitud)
		
		djs.save()
		
		return
		
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		
		self.insertaSimilitud(sim)
	
	#def reset(self):
		#"""Elimina todos los datos de la tabla de similitudes
		
		#ADVERTENCIA: usar sólo para pruebas del estudio de casos
		#"""
		#datos=DB()
		#consulta = "DELETE FROM similitudes"
		#datos.ejecutar (consulta)
		#return

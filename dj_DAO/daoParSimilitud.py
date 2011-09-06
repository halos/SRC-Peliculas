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
			
			if djs.Pel1.idPel not in similitudes:
				#si el item1 no está en el diccionario
				#se introduce con un diccionario vacío
				similitudes[djs.Pel1.idPel] = {}
				
			if djs.Pel2.idPel not in similitudes:
				#si el item1 no está en el diccionario
				#se introduce con un diccionario vacío
				similitudes[djs.Pel2.idPel] = {}

			
			ps = parSimilitud.ParSimilitud(djs.Pel1.idPel, djs.Pel2.idPel, djs.similitud)
			
			similitudes[djs.Pel1.idPel][djs.Pel2.idPel] = ps
			similitudes[djs.Pel2.idPel][djs.Pel1.idPel] = ps
			
		return similitudes
		
	def getSimilitudesItem(self,idPel):
		""" Obtiene todas las similitudes que implican un item en concreto
	
		Params:
	
			idPel(int): Identificador del item cuyas similitudes se buscan
	
		Return:
	
			(dict): {idPel:parSimilitud}
		"""
		
		djSimilitudes = []
		djSimilitudes += djModels.Similitud.objects.filter(Pel1=idPel)
		djSimilitudes += djModels.Similitud.objects.filter(Pel2=idPel)

		similitudes={}
		
		for djs in djSimilitudes:
			
			ps = parSimilitud.ParSimilitud(djs.Pel1.idPel, djs.Pel2.idPel, djs.similitud)
		
			if djs.Pel1.idPel != idPel:
				similitudes[djs.Pel1.idPel] = ps
		
			else:
				similitudes[djs.Pel2.idPel] = ps

		return similitudes

	def insertaSimilitud(self,sim):
		"""
		Inserta un nuevo par de similitud
		Params:
			sim: Similitud a insertar
		"""
		
		pel1 = djModels.Pelicula.objects.get(pk=sim.idP1)
		pel2 = djModels.Pelicula.objects.get(pk=sim.idP2)
		
		djs = djModels.Similitud(Pel1=pel1, Pel2=pel2, \
											similitud=sim.similitud)
		
		djs.save()
		
		return
	
	def insertaSimilitudes(self,sims):
		"""
		Inserta pares de similitud
		Params:
			sims: Similitudes a insertar
		"""
		
		for s in sims:
			self.insertaSimilitud(s)
	
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		
		sim_list = djModels.Similitud.objects.filter(Pel1=sim.idPel1, Pel2=sim.idPel2)
		
		if not sim_list:
			
			sim_list = djModels.Similitud.objects.filter(Pel1=sim.idPel2, Pel2=sim.idPel1)
		
			if not sim_list:
			
			self.insertaSimilitud(sim)
		
		sim_upd = sim_list[0]
		sim_upd.similitud = sim.similitud
		sim_upd.save()
	
	def actualizaSimilitudes(self,sims):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		
		for s in sims:
			self.actualizaSimilitud(s)

	def borraDB(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		
		Similitud.objects.all().delete()
		
	
	#def reset(self):
		#"""Elimina todos los datos de la tabla de similitudes
		
		#ADVERTENCIA: usar sólo para pruebas del estudio de casos
		#"""
		#datos=DB()
		#consulta = "DELETE FROM similitudes"
		#datos.ejecutar (consulta)
		#return

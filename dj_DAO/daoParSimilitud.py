#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from singleton import *
from django.db import connection, transaction

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
		
		del(djSimilitudes)
		
		return similitudes
		
	def getSimilitudesItem(self,idPel):
		""" Obtiene todas las similitudes que implican un item en concreto
	
		Params:
	
			idPel(int): Identificador del item cuyas similitudes se buscan
	
		Return:
	
			(dict): {idPel:parSimilitud}
		"""
		
		consulta = 'SELECT * FROM srcp_similitud \
					WHERE Pel1_id=%d OR Pel2_id=%d \
					ORDER BY similitud DESC LIMIT 7' % (idPel, idPel)
		#consulta = 'SELECT * FROM srcp_similitud WHERE Pel1_id=%d OR Pel2_id=%d' % (idPel, idPel)
		
		djSimilitudes = djModels.Similitud.objects.raw(consulta)
		
		similitudes={}
		
		for djs in djSimilitudes:
			
			ps = parSimilitud.ParSimilitud(djs.Pel1.idPel, djs.Pel2.idPel, djs.similitud)
		
			if djs.Pel1.idPel != idPel:
				similitudes[djs.Pel1.idPel] = ps
		
			else:
				similitudes[djs.Pel2.idPel] = ps
		
		del(djSimilitudes)
		
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
		
		print "Deshabilitando llaves"
		self.disableKeys()
		print "Llaves deshabilitadas"
		
		cursor = connection.cursor()
		consulta = "INSERT INTO srcp_similitud (Pel1_id, Pel2_id, similitud) VALUES "
		
		consulta += ', '.join( \
					['(%d ,%d, %.7r)' % (s.idP1, s.idP2, s.similitud) for s in sims] \
					)
			
		cursor.execute(consulta)
		transaction.commit_unless_managed()
		
		print "Habilitando llaves"
		self.enableKeys()
		print "Llaves habilitadas"
	
	def actualizaSimilitud(self,sim):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		
		cursor = connection.cursor()
		consulta = "UPDATE srcp_similitud SET similitud = %.7r WHERE \
						Pel1_id = %d AND Pel2_id = %d OR \
						Pel1_id = %d AND Pel2_id = %d" % \
						(sim.similitud, sim.idP1, sim.idP2, sim.idP2, sim.idP1)
						
		print "Se actualiza"
		cursor.execute(consulta)
		transaction.commit_unless_managed()
		print "Actualizada"
	
	def actualizaSimilitudes(self,sims):
		"""
		Actualiza el valor de similitud para una tupla ya existente
		Params:
			sim: similitud a actualizar
		"""
		
		sims_nuevas = []
		sims_act = []
		
		print "Buscando similitudes en la BDD"
		cont = 0
		
		for sim in sims:
			cont += 1
			if not cont % 100:
				print "Se buscaron %d similitudes" % (cont, )
			
			
				
			sim_list = djModels.Similitud.objects.filter(Pel1=sim.idP1, Pel2=sim.idP2)
			
			if not sim_list:
				sim_list = djModels.Similitud.objects.filter(Pel1=sim.idP2, Pel2=sim.idP1)
			
				if not sim_list:
					sims_nuevas.append(sim)
					
				else:
					sims_act.append(sim)
					
			else:
				
				sims_act.append(sim)
		
		print len(sims_act), "similitides a actualizar"
		print len(sims_nuevas), "similitudes nuevas"
		
		print "Desabilitando llaves"
		self.disableKeys()
		print "Llaves desabilitadas"
		
		print "Insertando similitides"
		self.insertaSimilitudes(sims_nuevas)
		
		print "Actualizando similitudes"
		for s in sims_act:
			self.actualizaSimilitud(s)
		
		print "Habilitando llaves"
		self.enableKeys()
		print "Llaves habilitadas"

	def borraDB(self):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		
		cursor = connection.cursor()
		consulta = 'DELETE FROM srcp_similitud'
		
		cursor.execute(consulta)
		transaction.commit_unless_managed()
		
		#djModels.Similitud.objects.all().delete()
				
	def enableKeys(self):
		""" Function doc
	
		Params:
	
			None
	
		Return:
	
			(Nonetype): None
		"""
		
		cursor = connection.cursor()
		
		cursor.execute('ALTER TABLE srcp_similitud ENABLE KEYS')
		transaction.commit_unless_managed()
		
	def disableKeys(self):
		""" Function doc
	
		Params:
	
			None
	
		Return:
	
			(Nonetype): None
		"""
		
		cursor = connection.cursor()
		
		cursor.execute('ALTER TABLE srcp_similitud DISABLE KEYS')
		transaction.commit_unless_managed()

	def estaSimilitud(self, sim):
		"""Comprueba si una similitud está en la BDD"""
		
		consulta = "SELECT * FROM srcp_similitud WHERE \
						Pel1_id = %d AND Pel2_id = %d OR \
						Pel1_id = %d AND Pel2_id = %d" % \
						(sim.idP1, sim.idP2, sim.idP2, sim.idP1)
		
		try:
			
			Similitud.objects.raw(consulta)[0]
			
		except IndexError:
			return False
		else:
			return True

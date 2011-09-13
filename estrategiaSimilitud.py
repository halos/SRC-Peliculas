#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#import os

#sys.path.append('..')
sys.path.append('dj_DAO')

import motor
#import settings
import singleton
import parSimilitud
import daoParSimilitud

#os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from srcp.models import Valoracion

class EstrategiaSimilitud: #(singleton):
	""" Interfaz de la estrategia de similitud """
	
	def __init__(self,  sim_func = None):
		""" Constructor. Cuando sea llamado después de ser creado con la 
		función de similitud, no se le pasa el parámetro
	
		Params:
	
			sim_func(function): Función de similitud que recibe una lista de
			valoraciones por parámetro
		"""
		
		if sim_func:
			self.__calcula_similitud = sim_func

	def similitud(self, _nuevasValoraciones=[]):
		""" Método para calcular la similitud entre películas
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
			_nuevasValoraciones(list): Lista con las nuevas valoraciones
	
		Return:
	
			None #(list): Lista de similitudes entre las películas (ParSimilitud)
		"""
		
		print "--> Entra en función similitud"
		daops = daoParSimilitud.DAOParSimilitud()
		
		# lista con los ParSimilitud
		paresSimilitud = []
		valoraciones = {}
		
		# borrar similitudes
		if not _nuevasValoraciones:
			print "--> Borra similitudes"
			daops.borraDB()
		
		print "Obteniendo todas las valoraciones"
		_valoraciones = Valoracion.objects.all()
		
		# Todas las películas
		# creación de la estructura de datos		
		#	dict{idPel:dict{idUsu:valoracion}}
		print "Se va a crear la estructura de datos"
		for v in _valoraciones:
			if v.Pel.idPel not in valoraciones:
				valoraciones[v.Pel.idPel] = {}
				
			valoraciones[v.Pel.idPel][v.Usu.idUsu] = v.puntuacion
		
		# obtención de los id de las películas
		print "Se obtienen las claves"
		p1 = valoraciones.keys()
		
		# Si se actualiza el modelo solo será para unas pocas peliculas
		if _nuevasValoraciones: # Se actualiza el modelo
			print "Se actualiza el modelo"
			p2 = list(set([v.idPel for v in _nuevasValoraciones]))
			print "Son", len(p2), "peliculas"
			
		else: # Se crea por primera vez el modelo de similitudes
			print "No se actualiza el modelo, se copian las claves"
			p2 = p1[:] # copia
		
		# Libera memoria
		del _valoraciones
		if _nuevasValoraciones:
			del _nuevasValoraciones
			# para las funciones que comprueban este parámetro
			_nuevasValoraciones = True
		
		cont = 0
		step = 100000
		
		# obtención de las valoraciones de cada usuario
		print "Se va a empezar a calcular las similitudes"
		for i in p1:
			
			if i in p2:
				p2.remove(i)

			for j in p2:
				similitud = self.__calcula_similitud(\
					valoraciones[i], valoraciones[j])
				ps = parSimilitud.ParSimilitud(i, j, similitud)
				paresSimilitud.append(ps)
				
				if len(paresSimilitud) == step:
					cont +=1
					print "Se van a guardar %d similitudes" % (step,)
					if not _nuevasValoraciones:
						daops.insertaSimilitudes(paresSimilitud)
					else:
						daops.actualizaSimilitudes(paresSimilitud)
					
					for ps in paresSimilitud: del ps
					del(paresSimilitud)
					paresSimilitud = []
					print "%d similitudes guardadas y memoria liberada" % (cont * step,)
		
		print "Guardando las últimas %d similitudes" % (len(paresSimilitud),)
		if not _nuevasValoraciones:
			daops.insertaSimilitudes(paresSimilitud)
		else:
			daops.actualizaSimilitudes(paresSimilitud)
		
		print 'Similitudes almacenadas'
		for ps in paresSimilitud: del ps
		del(paresSimilitud)
		
	def actualizaSimilitud(self, _nuevasValoraciones):
		""" Recalcula las similitudes en base a unas ya existentes y a las
		nuevas valoraciones 
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
			_nuevasValoraciones(list): Lista con las nuevas valoraciones
	
		Return:
	
			None #(list): Lista de similitudes entre las películas (ParSimilitud)
		"""
		
		# para que no se modifiquen las valoraciones en memoria
		#valoraciones = _valoraciones[:]
		
		# actualizar las valoraciones
		#for nv in _nuevasValoraciones:
			#if nv in valoraciones:
				#indice = valoraciones.index(nv)
				#valoraciones[indice].valoracion = nv.valoracion
			#else:
				#valoraciones.append(nv)
				
		# almacenar valoraciones actualizadas
		#daoValoracion.DAOValoracion.guarda(valoraciones)
		
		self.similitud(_nuevasValoraciones)

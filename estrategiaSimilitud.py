#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("DAO")

import motor
import parSimilitud
import metricas
import daoParSimilitud


class EstrategiaSimilitud:
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

	def insertaSimilitud(self, _valoraciones):
		"""Inserta las similitudes en base a las valoraciones, crea el modelo desde cero
	
		Params:
	
			_valoraciones(list): Lista con todas las valoraciones
	
		Return:
	
			None
		"""
		
		# lista con los ParSimilitud
		m = motor.Motor()
		paresSimilitud = []
		valDict = {}
		
		# para que no se modifiquen las valoraciones en memoria
		valoraciones = _valoraciones[:]
		
		#Borramos todas las similitudes de la BD (OJo!)
		print 'Borrando similitudes anteriores...'
		m.borraSimilitudes()
		# Desactivamos los índices para una inserción masiva, mucho más rápida
		daoParSimilitud.DAOParSimilitud().disableKeys()
		
		# Todas las películas
		# creación de la estructura de datos		
		#	dict{idPel:dict{idUsu:valoracion}}
		for i in valoraciones:
			if i.idPel not in valDict:
				valDict[i.idPel] = {}
				
			valDict[i.idPel][i.idUsu] = i.valoracion
		
		# obtención de los id de las películas
		p1 = valDict.keys()
		p2 = p1[:] # copia
		
		# Se crea por primera vez el modelo de similitudes
		print 'Comienza el cálculo de similitudes'
		for i in p1:
			if i in p2:
				p2.remove(i)
			for j in p2:
				similitud = self.__calcula_similitud(\
					valDict[i], valDict[j])
				ps = parSimilitud.ParSimilitud(i, j, similitud)
				paresSimilitud.append(ps)
				
			# Descargamos similitudes en la BD
			if len(paresSimilitud) >= 1000000:
				m.insertaSimilitudes(paresSimilitud)
				paresSimilitud = [] # Vaciamos la lista, ya descargada en la BD
				
		# Descargamos el resto
		if len(paresSimilitud) > 0:
			m.insertaSimilitudes(paresSimilitud)
				
		print 'Fin del cálculo de similitudes\n'	 
		#return paresSimilitud
		
		print 'Regeneramos índices...'
		t_inic = metricas.get_clock()
		daoParSimilitud.DAOParSimilitud().enableKeys()
		t_fin = metricas.get_clock()
		print 'Tiempo utilizado para generar índices: %f' % (t_fin - t_inic) 
		
	
	def actualizaSimilitud(self, _valoraciones, _nuevasValoraciones):
		""" Recalcula las similitudes en base a unas ya existentes y a las
		nuevas valoraciones 
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
			_nuevasValoraciones(list): Lista con las nuevas valoraciones
	
		Return:
	
			None #(list): Lista de similitudes entre las películas (ParSimilitud)
		"""
		if _nuevasValoraciones: # No hay nada que hacer
			print 'No hay nuevas valoraciones que aportar'
			return
		
		# para que no se modifiquen las valoraciones en memoria
		valoraciones = _valoraciones[:]
		
		# actualizar las valoraciones
		for nv in _nuevasValoraciones:
			if nv in valoraciones:
				indice = valoraciones.index(nv)
				valoraciones[indice].valoracion = nv.valoracion
			else:
				valoraciones.append(nv)
		
		# lista con los ParSimilitud
		paresSimilitud = []
		valDict = {}
		
		# Todas las películas
		# creación de la estructura de datos		
		#	dict{idPel:dict{idUsu:valoracion}}
		for i in _valoraciones:
			if i.idPel not in valDict:
				valDict[i.idPel] = {}
			
			valDict[i.idPel][i.idUsu] = i.valoracion
		
		# obtención de los id de las películas
		p1 = valDict.keys()
		
		# Si se actualiza el modelo solo será para unas pocas peliculas
		p2 = list(set([v.idPel for v in _nuevasValoraciones]))
			
		# obtención de las valoraciones de cada usuario
		print 'Comienza el cálculo de similitudes'
		for i in p1:
			if i in p2:
				p2.remove(i)
			for j in p2:
				similitud = self.__calcula_similitud(\
					valDict[i], valDict[j])
				ps = parSimilitud.ParSimilitud(i, j, similitud)
				paresSimilitud.append(ps)
				
			# Descargamos similitudes en la BD
			if len(paresSimilitud) >= 1000000:
				self.almacenaSimilitudes(paresSimilitud)
				paresSimilitud = [] # Vaciamos la lista, ya descargada en la BD
				

		# Descargamos el resto
		if len(paresSimilitud) > 0:
			self.almacenaSimilitudes(paresSimilitud)
		print 'Fin del cálculo\n'
		
		
		def almacenaSimilitudes(self, _paresSimilitud):
			""" Almacena las similitudes calculadas teniendo en cuenta, si hay que
				insertarlas o actualizarlas
		
			Params:
		
				_paresSimilitud(list): Lista con las similitudes a actualizar o insertar
		
			Return:
		
				None
			"""
			m = motor.Motor()
			
			# Almacenamos las similitudes
			sim_insertar = []
			sim_actualizar = []
			sim_anteriores = m.getSimilitudes()
	
			for s in _paresSimilitud:
				if s in sim_anteriores:
					sim_actualizar.append(s)
				else:
					sim_insertar.append(s)
					
			m.insertaSimilitudes(sim_insertar)
			m.actualizaSimilitudes(sim_actualizar)
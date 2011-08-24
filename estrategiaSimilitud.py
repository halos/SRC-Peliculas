#!/usr/bin/python
# -*- coding: utf-8 -*-

import motor
import parSimilitud

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

	def similitud(self, _valoraciones, _nuevasValoraciones=[]):
		""" Método para calcular la similitud entre películas
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
			_nuevasValoraciones(list): Lista con las nuevas valoraciones
	
		Return:
	
			None #(list): Lista de similitudes entre las películas (ParSimilitud)
		"""
		
		# lista con los ParSimilitud
		paresSimilitud = []
		valoraciones = {}
		
		# Todas las películas
		# creación de la estructura de datos		
		#	dict{idPel:dict{idUsu:valoracion}}
		for i in _valoraciones:
			if i.idPel not in valoraciones:
				valoraciones[i.idPel] = {}
				
			valoraciones[i.idPel][i.idUsu] = i.valoracion
		
		# obtención de los id de las películas
		p1 = valoraciones.keys()
		
		
		# Si se actualiza el modelo solo será para unas pocas peliculas
		if _nuevasValoraciones: # Se actualiza el modelo
			p2 = list(set([v.idPel for v in _nuevasValoraciones]))
			
		else: # Se crea por primera vez el modelo de similitudes
			p2 = p1[:] # copia
			
		# obtención de las valoraciones de cada usuario
		print 'Comienza el cálculo de similtudes'
		for i in p1:
			if i in p2:
				p2.remove(i)
			for j in p2:
				similitud = self.__calcula_similitud(\
					valoraciones[i], valoraciones[j])
				ps = parSimilitud.ParSimilitud(i, j, similitud)
				paresSimilitud.append(ps)
		print 'Fin del cálculo\n'
		#return paresSimilitud
		# almacenamiento de similitudes
		m = motor.Motor()
		
		sim_insertar = []
		sim_actualizar = []
		sim_anteriores = m.getSimilitudes()
		
		for s in paresSimilitud:
			if s in sim_anteriores:
				sim_actualizar.append(s)
			else:
				sim_insertar.append(s)
		
		m.insertaSimilitudes(sim_insertar)
		m.actualizaSimilitudes(sim_actualizar)
		
	def actualizaSimilitud(self, _valoraciones, _nuevasValoraciones):
		""" Recalcula las similitudes en base a unas ya existentes y a las
		nuevas valoraciones 
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
			_nuevasValoraciones(list): Lista con las nuevas valoraciones
	
		Return:
	
			None #(list): Lista de similitudes entre las películas (ParSimilitud)
		"""
		
		# para que no se modifiquen las valoraciones en memoria
		valoraciones = _valoraciones[:]
		
		# actualizar las valoraciones
		for nv in _nuevasValoraciones:
			if nv in valoraciones:
				indice = valoraciones.index(nv)
				valoraciones[indice].valoracion = nv.valoracion
			else:
				valoraciones.append(nv)
		# almacenar valoraciones actualizadas
		#daoValoracion.DAOValoracion.guarda(valoraciones)
		
		self.similitud(valoraciones, _nuevasValoraciones)

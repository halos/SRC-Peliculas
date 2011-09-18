#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append('dj_DAO')

import singleton
import parSimilitud
import daoParSimilitud

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

	def similitud(self):
		""" Método para calcular la similitud entre películas
	
		Params:
	
			_valoraciones(list): Lista con las valoraciones de los usuarios
	
		Return:
	
			None
		"""
		
		print "--> Entra en función similitud"
		daops = daoParSimilitud.DAOParSimilitud()
		
		# lista con los ParSimilitud
		paresSimilitud = []
		valoraciones = {}
		
		# borrar similitudes
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
		
		p2 = p1[:] # copia
		
		# Libera memoria
		del _valoraciones
		
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
					daops.insertaSimilitudes(paresSimilitud)
					
					for ps in paresSimilitud: del ps
					del(paresSimilitud)
					paresSimilitud = []
					print "%d similitudes guardadas y memoria liberada" % (cont * step,)
		
		print "Guardando las últimas %d similitudes" % (len(paresSimilitud),)
		daops.insertaSimilitudes(paresSimilitud)
		
		print 'Similitudes almacenadas'
		for ps in paresSimilitud: del ps
		del(paresSimilitud)

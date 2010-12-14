#!/usr/bin/python
# -*- coding: utf-8 -*-

from parSimilitud import ParSimilitud

class EstrategiaSimilitud:
	""" Interfaz de la estrategia de similitud """
	
	def __init__(self,  sim_func):
		""" Constructor
	
		Params:
	
			sim_func(function): Función de similitud que recibe una lista de
			valoraciones por parámetro
		"""
		
		self.__calcula_similitud = sim_func

	def similitud(self, _valoraciones):
		""" Function doc
	
		Params:
	
			valoraciones(list): Lista con las valoraciones de los usuarios
	
		Return:
	
			(list): Lista de similitudes entre los usuarios
		"""
		
		# lista con los ParSimilitud
		paresSimilitud = []
		valoraciones = {}
		
		#creación de la estructura de datos		
		#	dict{idPel:dict{idUsu:valoracion}}
		for i in _valoraciones:
			if i.idPel not in valoraciones:
				valoraciones[i.idPel] = {}
				
			valoraciones[i.idPel][i.idUsu] = i.valoracion
		
		# obtención de los id de las películas
		p1 = valoraciones.keys()
		p2 = p1[:] # copia
		
		# obtención de las valoraciones de cada usuario
		
		for i in p1:
			p2.remove(i)
			for j in p2:
				similitud = self.__calcula_similitud(valoraciones[i], valoraciones[j])
				ps = ParSimilitud(i, j, similitud)
				paresSimilitud.append(ps)
		
		return paresSimilitud

#!/usr/bin/python
# -*- coding: utf-8 -*-


class EstrategiaSimilitud:
	""" Interfaz de la estrategia de similitud """
	
		def __init__(self,  sim_func):
		""" Constructor
	
		Params:
	
			sim_func(): Función de similitud que recibe una lista de
			valoraciones por parámetro
		"""
		
		self.__calcula_parSimilitud = sim_func

	def similitud(self, valoraciones):
		""" Function doc
	
		Params:
	
			valoraciones(list): Lista con las valoraciones de los usuarios
	
		Return:
	
			(list): Lista de similitudes entre los usuarios
		"""
		
		similitudes = {} # lista con los ParSimilitud
		
		#creación de la estructura de datos
		#	dict{idusu:dict{idPel:valoracion}}
		for i in valoraciones:
			if i.idUsu not in similitudes:
				similitudes[i.idUsu] = {}
				
			similitudes[i.idUsu][i.idPel] = i.valoracion
		
		# obtención de usuarios
		u1 = vals_per_usu.keys()
		u2 = u1[:] # copia
		
		# obtención de las valoraciones de cada usuario
		for i in u1:
			del u2[i]
			for j in u2:
				similitudes.append(self.__calcula_parSimilitud(i, j)
		
		return similitudes

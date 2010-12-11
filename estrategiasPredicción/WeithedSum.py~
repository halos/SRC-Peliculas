#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

def class WeithedSum:
    
	""" Clase que implementa el método de prediccion WeithedSum """

	def __init__(self, idUsu):
		""" Constructor
		
		Params: 
			
			idUsu: Identificador del usuario registrado en el sistema

		"""
	
		self.idUsu = idUsu

	def predice(self, idItem, similitudes, valoraciones):
		"""
			
		Metodo que devuelve el valor de prediccion para un item-usuario
		
		Params:
		
				idItem: Identificador del item cuyo valora deseamos predecir
				valoraciones(dict): Contiene todos las valoraciones aportadas por todos los usuarios
				similitudes(dict): Contiene los pares de similitud entre items devueltos por el agrupamiento	

		Return:
					
				prediccion(Valoracion): Valoración predicha para un valor desconocido
					
		"""
		
		suma_denom = 0
		suma_num = 0
		lvaloraciones = valoraciones.get(self.idUsu).values()

		"Cálculo de la fórmula de la prediccion"

		"Calculo del denominador"

		for similitud in similitudes:
			idItem2 = similitud.getItems().get(similitud.getItems().index(idItem) - 1)
			if lvaloraciones.get(idItem2) != 0:
				suma_denom += similitud.getVal()
	
		"Cálculo del numerador"
	  
		for similitud in similitudes:
			idItem2 = similitud.getAtributes().get(similitud.getAtributes().index(idItem) - 1)
			if lvaloraciones.get(idItem2) != 0:
				suma_num += similitud.getVal() * lvaloraciones.get(idItem2).getVal()
	
		vprediccion = suma_num / suma_denom
		
		return Valoracion(self.idUsu, idItem, vprediccion)


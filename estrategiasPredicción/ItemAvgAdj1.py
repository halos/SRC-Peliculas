#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="sramirez"
__date__ ="$07-dic-2010 10:22:31$"

from math import fabs

def class ItemAvgAdj1:
    
	""" Clase que implementa el método de prediccion Item Average Adjustament (All-1) """

	def __init__(self, idUsu):
		""" Constructor
		
		Params: 
			
			idUsu: Identificador del usuario registrado en el sistema

		"""
		
		self.idUsu = idUsu


	def mediausuario(self, valoraciones):
		"""
			Metodo que calcula la media de las valoraciones hechas por un usuario a todos sus items
			
			Params:
					
					valoraciones(dict): Valoraciones hechas por todos los usuarios para todos los items
					
			Return:
					media_usuario: Media de las valoraciones hechas por un usuario a todos sus items
			
		"""
			
		lval_usuario = valoraciones.get(self.idUsu)
		nval = 0
		media_usuario = 0
		for valoracion in lval_usuario:
			if valoracion.getVal()	!= 0:
				media_usuario += valoracion.getVal()
			nval+= 1
		media_usuario = media_usuario / nval
		return media_usuario

	def mediaitem(self, idItem, valoraciones):

		"""
			Metodo que calcula la media de las valoraciones hechas para un determinado item
			Params:
					
					valoraciones(dict): Valoraciones hechas por todos los usuarios para todos los items
					
			Return:
					media_usuario: Media de las valoraciones hechas para un determinado item
			
		"""
		
		media_item = 0
		nval = 0
		for lvaloracion in valoraciones.values():
			item = lvaloracion.get(idItem)
			if item.getVal() != 0:
				media_item += item.getVal()
			nval += 1
		media_item = media_item / nval
		return media_item

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
	

        media_item = mediaitem(valoraciones)
        media_usuario = mediausuario(valoraciones)
        suma_denom = 0
		suma_num = 0

		"Cálculo de la fórmula de la prediccion"

		"Cálculo del denominador"

		lsimilares = similitudes.get(idItem).values()
		lvaloraciones = valoraciones.get(self.idUsu).values()

		for i in range(lsimilares):
			if lvaloraciones[i] != 0:
				suma_denom += math.fabs(lsimilares[i])
				
		"Cálculo del numerador"
		  
			for i in range(lvaloraciones):
				if lvaloraciones[i] != 0:
					suma_num += lsimilares[i].getVal() * (valoraciones[i].getVal() - media_usuario)
		
		vprediccion = suma_num / suma_denom + media_item
			
		return Valoracion(self.idUsu, idItem, vprediccion)


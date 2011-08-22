#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from singleton import *

sys.path.append('..')

import usuario
import srcp.models as djModels


class DAOUsuario(Singleton):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		pass
	
	def getUsuarios(self):
		"""
		metodo que devuelve todos los usuarios registrados en la aplicacion
		
		"""
		
		djUsus = djModels.Usuario.objects.all()
		
		usus=[]
		
		for dju in djUsus:
			u = usuario.Usuario(dju.idUsu, dju.clave)
			usus.append(u)
		
		return usus
	
	def getUsuario(self,id):
		"""
		metodo que busca un usuario concreto
		Params:
			id: identificador del usuario a buscar
		"""
		
		usu = None
		
		try:
		
			dju = djModels.Usuario.objects.get(idUsu = id)
			usu = usuario.Usuario(dju.idUsu, dju.clave)
		
		except djModels.Usuario.DoesNotExist:
			
			pass
			
		finally:
		
			return usu
	
	def insertar(self,usu):
		"""
		Introduce un nuevo usuario en el sistema
		Params:
			usu: usuario a insertar
		"""
		
		dju = djModels.Usuario(idUsu=usu.idUsu, clave=usu.passw)
		dju.save()

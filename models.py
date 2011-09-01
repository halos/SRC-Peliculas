# -*- coding: utf-8 -*-

from django.db import models

# Modelos de SRC PeliculasCreate

class Pelicula(models.Model):
	idPel = models.PositiveIntegerField(primary_key=True)
	titulo = models.CharField(max_length=255)
	anio = models.PositiveIntegerField()
	
	def get_valoracion_usu(self, usu):
		""" Obtiene la valoración del usuario dado a esta película
	
		Params:
	
			usu(Usuario): Usuario que ha valorado esta película
	
		Return:
	
			(int): Valoración (int) 0 si no se ha valorado
		"""
		
		try:
			
			valoracion = p.valoracion_set.all().get(Usu=usu).puntuacion
			
		except Valoracion.DoesNotExist:
			
			valoracion = 0
		
		finally:
			
			return valoracion
		
	def __unicode__(self):
		
		return self.titulo	
	
class Usuario(models.Model):
	idUsu = models.PositiveIntegerField(primary_key=True)
	clave = models.CharField(max_length=32) # md5
	
	def __unicode__(self):
		return str(self.idUsu)
		
	
class Valoracion(models.Model):
	Pel = models.ForeignKey(Pelicula)
	Usu = models.ForeignKey(Usuario)
	puntuacion= models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		
		return str(self.Usu.idUsu) + ' - ' + self.Pel.titulo
	
class Similitud(models.Model):
	Pel1 = models.ForeignKey(Pelicula, related_name='sim_idPel1')
	Pel2 = models.ForeignKey(Pelicula, related_name='sim_idPel2')
	similitud = models.DecimalField(max_digits=6, decimal_places=5)
	
	def __unicode__(self):
		
		return self.Pel1.titulo + ' - ' + self.Pel2.titulo

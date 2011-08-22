from django.db import models

# Modelos de SRC PeliculasCreate

class Pelicula(models.Model):
	idPel = models.PositiveIntegerField(primary_key=True)
	titulo = models.CharField(max_length=255)
	anio = models.PositiveIntegerField()
	
	def __unicode__(self):
		
		return self.titulo	
	
class Usuario(models.Model):
	idUsu = models.PositiveIntegerField(primary_key=True)
	
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

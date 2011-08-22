from srcp.models import Pelicula, Usuario, Similitud, Valoracion
from django.contrib import admin

class ValoracionesInline(admin.StackedInline):
	model = Valoracion
	extra = 5

class PeliculaAdmin(admin.ModelAdmin):
	fields = ['titulo', 'idPel', 'anio']
	list_display = ('titulo', 'idPel', 'anio')
	
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ('idUsu', )
	inlines = [ValoracionesInline]

admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Similitud)
admin.site.register(Valoracion)

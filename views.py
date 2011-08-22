from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect #, HttpResponse
from django.core.urlresolvers import reverse
#from django.template import RequestContext

from srcp.models import Pelicula, Usuario, Valoracion, Similitud


def login(request):
	
	u = Usuario.objects.get(username__exact=request.POST['nombre'])
	context = {}
	
	if u.clave == request.POST['clave']:
		
		request.session['idUsu'] = m.idUsu
		
		return render_to_response('srcp/indice.html', context)
	
	else:
		
		context['error'] = 'Login incorrecto'
		
		return render_to_response('srcp/login.html', context)

def logout(request):
	
	context = {}
	
	try:
		
		del request.session['idUsu']
		
		return render_to_response('srcp/login.html', context)
		
	except KeyError:
		
		pass
	
	return HttpResponse("You're logged out.")

def indice(request):

	estra_pred = None
	recomendaciones = self.recomendar(estra_pred)
	
	context = {
		'recomendaciones': recomendaciones
	}
	
	return render_to_response('srcp/index.html', context)

def valorar(request, idPel):
	
	context = {}

	try:
	
		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)
		punt = int(request.POST['puntuacion'])
	
	except (KeyError, Valoracion.DoesNotExist):
	
		# Redisplay the poll voting form.
		#context['pelicula'] = p
		context['error'] = "Error al seleccionar pelicula."
		
		return render_to_response('srcp/indice.html', context)
	
	else:
	
		v = Valoracion(Pel=pel, Usu=usu, puntuacion=punt)
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('srcp.views.results', args=(p.id,)))

def buscar(request):
	
	pass

def get_recomendaciones(request):
	
	pass

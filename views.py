from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from srcp.models import Pelicula, Usuario, Valoracion, Similitud


def login(request):
	pass

def indice(request):
	
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	
	context = {
		'latest_poll_list': latest_poll_list,
		'title': 'indice de encuestas',
		'body': 'Aqui encontrara el indice de encuestas',
	}
	
	return render_to_response('learn/index.html', context)
	
def detail(request, poll_id):
	
	poll = get_object_or_404(Poll, pk=poll_id)
	
	context = {
		'title': 'Detalle de encuesta',
		'body': 'Aqui encontrara el indice de encuestas',
		'poll': poll,
	}
	
	return render_to_response('learn/detail.html', context,
							   context_instance=RequestContext(request))

def results(request, poll_id):
	
	context = {
		'title': 'Resultados de la encuesta %s' % (poll_id, ),
		'body': 'Resultados de la encuesta %s' % (poll_id, ),
	}
	
	return render_to_response('learn/index.html', context)
	
def valorar(request, idPel):
	
	context = {
		'title': 'Votar',
		'body': 'Vote en la encuesta %s' % (poll_id, ),
	}

	try:
	
		pel = get_object_or_404(Pelicula, pk=idPel)
		usu = get_object_or_404(Usuario, pk=idUsu)
		punt = int(request.POST['puntuacion'])
	
	except (KeyError, Valoracion.DoesNotExist):
	
		# Redisplay the poll voting form.
		#context['pelicula'] = p
		context['error_message'] = "Error al seleccionar pelicula."
		
		return render_to_response('srcp/indice.html', context,
									context_instance=RequestContext(request)
		)
	
	else:
	
		v = Valoracion(Pel=pel, Usu=usu, puntuacion=punt)
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('learn.views.results', args=(p.id,)))

def buscar(request):
	
	pass

def get_recomendaciones(request):
	
	pass

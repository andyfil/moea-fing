from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Salon, Pc, LecturaTop

class IndexView(generic.ListView):
    template_name = 'maquinas/index.html'
    context_object_name = 'latest_pc_list'

    def get_queryset(self):
        """Return the last five published pc."""
        return Pc.objects.order_by('-salon')[:5]


class DetailView(generic.DetailView):
    model = Pc
    template_name = 'maquinas/detail.html'


class ResultsView(generic.DetailView):
    #model = LecturaTop
    template_name = 'maquinas/results.html'

def results(request, pc_id):
    pc = get_object_or_404(Pc, pk=pc_id)
    # Obtengo todas las lecturas de la Pc
    lecturas = pc.lecturatop_set.all()
    #Armo los datos para graficar
    dataCantidadUsuarios = "indice,Lecturas\n"
    dataPorcentajeCpu = "indice,Lecturas\n"
    dataPorcentajeMemoria = "indice,Lecturas\n"
    for indice in range(len(lecturas)):
    	datoCU = str(indice) + "," + str(lecturas[indice].cant_usuarios) + "\n"
    	datoPCpu = str(indice) + "," + str(lecturas[indice].cpu_perc) + "\n"
    	datoPM = str(indice) + "," + str(lecturas[indice].mem_perc) + "\n"
    	dataCantidadUsuarios += datoCU
    	dataPorcentajeCpu += datoPCpu
    	dataPorcentajeMemoria += datoPM
    
    return render(request, 'maquinas/results.html', {'pc': pc, 'dataCantidadUsuarios': dataCantidadUsuarios, 'dataPorcentajeCpu':dataPorcentajeCpu, 
    												'dataPorcentajeMemoria':dataPorcentajeMemoria})
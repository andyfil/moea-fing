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
    data = "Cantidad,Lectura\n" + "1,5\n" + "2,2\n" + "3,4\n" + "4,7\n" + "5,3\n" + "6,8\n" + "7,5\n" + "8,6\n"
    return render(request, 'maquinas/results.html', {'pc': pc, 'data': data})
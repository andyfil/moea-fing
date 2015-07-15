from django.http import HttpResponseRedirect, HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from maquinas.forms import UsuarioTareaForm
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Salon, Pc, LecturaTop
from django.db import connection
from maquinas.forms import BigForm


@login_required
def bigform(request):

    #form = UsuarioTareaForm()
    form = BigForm()
    field1 = ""
    field2 = ""
    field3 = None
    if request.method == 'POST':
        #form = UsuarioTareaForm(request.POST, request.FILES)
        form = BigForm(request.POST, request.FILES)
        if form.is_valid():
            field1 = form.cleaned_data.get('field1')
            field2 = form.cleaned_data.get('field2')
            field3 = form.cleaned_data.get('field3') 
            #form.save()

    else:
        #form = UsuarioTareaForm()
        form = BigForm()

    context = {
        'form': form,
        'field1': field1,
        'field2': field2,
        'field3': field3,
    }

    return render_to_response('bigform.html', context, context_instance=RequestContext(request))

class IndexView(generic.ListView):
    template_name = 'maquinas\index.html'
    context_object_name = 'latest_pc_list'

    def get_queryset(self):
        return Pc.objects.order_by('-salon')


class DetailView(generic.DetailView):
    model = Pc
    template_name = 'maquinas/detail.html'


class ResultsView(generic.DetailView):
    #model = LecturaTop
    template_name = 'maquinas/results.html'

# def results_original(request, pc_id):
#     pc = get_object_or_404(Pc, pk=pc_id)
#     # Prueba de stored procedures
#     ultimosDatos = ""
#     id = 12
#     result_set = []
#     args = [id, ultimosDatos]
#     cursor = connection.cursor()
#     try:
#         cursor.callproc('obtenerUltimosDatos', args)
#         ultimosDatos = cursor.fetchall()
#         print result_set
#         print mac
#     finally:
#         cursor.close()

#     # TODO: Parsear ultimosDatos

#     # Obtengo todas las lecturas de la Pc
#     lecturas = pc.lecturatop_set.all()[:5]
#     #Armo los datos para graficar
#     dataCantidadUsuarios = "indice,Lecturas\n"
#     dataPorcentajeCpu = "indice,Lecturas\n"
#     dataPorcentajeMemoria = "indice,Lecturas\n"
#     for indice in range(len(lecturas)):
#     	datoCU = str(indice) + "," + str(lecturas[indice].cant_usuarios) + "\n"
#     	datoPCpu = str(indice) + "," + str(lecturas[indice].cpu_perc) + "\n"
#     	datoPM = str(indice) + "," + str(lecturas[indice].mem_perc) + "\n"
#     	dataCantidadUsuarios += datoCU
#     	dataPorcentajeCpu += datoPCpu
#     	dataPorcentajeMemoria += datoPM
#     if request.is_ajax():
#         template = 'maquinas/partial-results.html'
#     else:
#         template = 'maquinas/results.html'
#     return render(request, template, {'pc': pc, 'dataCantidadUsuarios': dataCantidadUsuarios, 'dataPorcentajeCpu':dataPorcentajeCpu, 
#     												'dataPorcentajeMemoria':dataPorcentajeMemoria, 'mac':mac})


def results(request, pc_id):
	#for dato in LecturaTop.objects.raw('SELECT * FROM maquinas_lecturatop WHERE pc_id = %s LIMIT 240', [pc_id]):
	#cursor = connection.cursor()
    #cursor.execute("SELECT * FROM datos WHERE pc = %s", [nombre])
    #lecturas = cursor.fetchall()
	
    pc = get_object_or_404(Pc, pk=pc_id)
    #Graficamos por periodos (4)
    periodoVisualizacion = 60 # 1 hora
    primera = periodoVisualizacion*0 + 1
    segunda = periodoVisualizacion*1 + 1
    tercera = periodoVisualizacion*2 + 1
    cuarta = periodoVisualizacion*3 + 1
    quinta = periodoVisualizacion*4 + 1
    indice = 1
    cantU_1=cantM_1=cantC_1=cantU_2=cantM_2=cantC_2=cantU_3=cantM_3=cantC_3=cantU_4=cantM_4=cantC_4 = 0

    # Obtengo las ultimas 4*periodoVisualizacion lecturas (4 periodos) de la Pc con id=pc_id
    lecturas = pc.datos_set.all().order_by('-id')[:periodoVisualizacion*4]
    
    for dato in lecturas:
        if (indice in range(cuarta, quinta)):
            cantU_1 = cantU_1 + dato.users
            cantM_1 = cantM_1 + dato.memory_use
            cantC_1 = cantC_1 + dato.cpu_use
            print "Dato " + str(indice) + ": " + str(dato.users) + " usuarios, " + str(dato.memory_use) + " memoria, " + str(dato.cpu_use) + " cpu" + "\n"
        if (indice in range(tercera, cuarta)):
            cantU_2 = cantU_2 + dato.users
            cantM_2 = cantM_2 + dato.memory_use
            cantC_2 = cantC_2 + dato.cpu_use
            print "Dato " + str(indice) + ": " + str(dato.users) + " usuarios, " + str(dato.memory_use) + " memoria, " + str(dato.cpu_use) + " cpu" + "\n"
        if (indice in range(segunda, tercera)):
            cantU_3 = cantU_3 + dato.users
            cantM_3 = cantM_3 + dato.memory_use
            cantC_3 = cantC_3 + dato.cpu_use
            print "Dato " + str(indice) + ": " + str(dato.users) + " usuarios, " + str(dato.memory_use) + " memoria, " + str(dato.cpu_use) + " cpu" + "\n"
        if (indice in range(primera, segunda)):
            cantU_4 = cantU_4 + dato.users
            cantM_4 = cantM_4 + dato.memory_use
            cantC_4 = cantC_4 + dato.cpu_use
            print "Dato " + str(indice) + ": " + str(dato.users) + " usuarios, " + str(dato.memory_use) + " memoria, " + str(dato.cpu_use) + " cpu" + "\n"

        indice = indice + 1

	# Calculo los promedios por horas
    promU_1 = cantU_1 / periodoVisualizacion
    promM_1 = cantM_1 / periodoVisualizacion
    promC_1 = cantC_1 / periodoVisualizacion
    promU_2 = cantU_2 / periodoVisualizacion
    promM_2 = cantM_2 / periodoVisualizacion
    promC_2 = cantC_2 / periodoVisualizacion
    promU_3 = cantU_3 / periodoVisualizacion
    promM_3 = cantM_3 / periodoVisualizacion
    promC_3 = cantC_3 / periodoVisualizacion
    promU_4 = cantU_4 / periodoVisualizacion
    promM_4 = cantM_4 / periodoVisualizacion
    promC_4 = cantC_4 / periodoVisualizacion
    
    #Armo los datos para graficar
    dataCantidadUsuarios = "indice,Lecturas\n"
    dataPorcentajeCpu = "indice,Lecturas\n"
    dataPorcentajeMemoria = "indice,Lecturas\n"
    
    datoCU = str(1) + "," + str(promU_1) + "\n"
    datoPCpu = str(1) + "," + str(promC_1) + "\n"
    datoPM = str(1) + "," + str(promM_1) + "\n"
    dataCantidadUsuarios += datoCU
    dataPorcentajeCpu += datoPCpu
    dataPorcentajeMemoria += datoPM
    
    datoCU = str(2) + "," + str(promU_2) + "\n"
    datoPCpu = str(2) + "," + str(promC_2) + "\n"
    datoPM = str(2) + "," + str(promM_2) + "\n"
    dataCantidadUsuarios += datoCU
    dataPorcentajeCpu += datoPCpu
    dataPorcentajeMemoria += datoPM
    
    datoCU = str(3) + "," + str(promU_3) + "\n"
    datoPCpu = str(3) + "," + str(promC_3) + "\n"
    datoPM = str(3) + "," + str(promM_3) + "\n"
    dataCantidadUsuarios += datoCU
    dataPorcentajeCpu += datoPCpu
    dataPorcentajeMemoria += datoPM
    
    datoCU = str(4) + "," + str(promU_4) + "\n"
    datoPCpu = str(4) + "," + str(promC_4) + "\n"
    datoPM = str(4) + "," + str(promM_4) + "\n"
    dataCantidadUsuarios += datoCU
    dataPorcentajeCpu += datoPCpu
    dataPorcentajeMemoria += datoPM

	# TODO: corregir esto para reenderizar solo la parte de las graficas utilizando ajax
    if request.is_ajax():
        template = 'maquinas/partial-results.html'
    else:
        template = 'maquinas/results.html'
    return render(request, template, {'pc': pc, 'dataCantidadUsuarios': dataCantidadUsuarios, 'dataPorcentajeCpu':dataPorcentajeCpu, 
                                                    'dataPorcentajeMemoria':dataPorcentajeMemoria})

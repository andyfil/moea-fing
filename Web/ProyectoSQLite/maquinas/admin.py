# from maquinas.models import Salon, Pc, Datos
# from django.contrib import admin

# class DatosInline(admin.TabularInline):
# 	model = Datos
# 	extra = 3

# class PcInline(admin.TabularInline):
# 	model = Pc
# 	extra = 3

# #class LecturaTopAdmin(admin.ModelAdmin):
# #	list_display = ('pc', 'tiempo_lectura', 'cant_usuarios', 'mem_perc', 'cpu_perc')
# #	list_filter = ['cant_usuarios']
# #	search_fields = ['pc']

# class PcAdmin(admin.ModelAdmin):
# 	#list_display = ('salon', 'nombre', 'ip', 'mac', 'so', 'ram', 'cpu', 'arq', 'estado')
# 	list_filter = ['estado']
# 	search_fields = ['salon']
# 	inlines = [DatosInline]

# class SalonAdmin(admin.ModelAdmin):
# 	list_display = ('prioridad', 'lugar', 'nombre')
# 	list_filter = ['prioridad']
# 	search_fields = ['lugar']
# 	inlines = [PcInline]

# admin.site.register(Salon, SalonAdmin)
# admin.site.register(Pc, PcAdmin)

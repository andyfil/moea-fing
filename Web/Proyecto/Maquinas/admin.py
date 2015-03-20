from Maquinas.models import Salon, PC, RegistroPC
from django.contrib import admin

class ResgistroPCInLine(admin.TabularInline):
	model = RegistroPC

class PCAdmin(admin.ModelAdmin):
	#fieldsets = [
	#	(None,               {'fields': ['question']}),
	#	('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	#]
	list_display = ('salon', 'nombre', 'mac', 'so', 'ram', 'cpu', 'estado', 'cant_usuarios')
	inlines = [ResgistroPCInLine]
	list_filter = ['cant_usuarios']
	search_fields = ['salon']

class PCInline(admin.TabularInline):
	model = PC
	extra = 3

class SalonAdmin(admin.ModelAdmin):
	#fieldsets = [
	#	(None,               {'fields': ['question']}),
	#	('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	#]
	list_display = ('prioridad', 'lugar', 'nombre')
	inlines = [PCInline]
	list_filter = ['prioridad']
	search_fields = ['lugar']
	
admin.site.register(Salon, SalonAdmin)
admin.site.register(PC, PCAdmin)
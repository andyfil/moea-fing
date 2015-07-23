from django import forms
from maquinas.models import UsuarioTarea

class UsuarioTareaForm(forms.ModelForm):
	class Meta:
		model = UsuarioTarea

	def clean_archivo(self):
		archivo = self.cleaned_data['archivo']
		#import pdb; pdb.set_trace()
		if archivo.name.split('.')[-1] != 'txt':
			raise forms.ValidationError('Solo se permiten archivos txt')

		return archivo
from django import forms
from maquinas.models import UsuarioTarea


# class BigForm(forms.Form):
# 	# field1 = forms.CharField()
# 	# field2 = forms.IntegerField()
# 	field3 = forms.FileField()

# 	def clean_field3(self):
# 		field3 = self.cleaned_data['field3']
# 		#import pdb; pdb.set_trace()
# 		if field3.name.split('.')[-1] != 'png':
# 			raise forms.ValidationError('Solo se permiten archivos png')

# 		return field3

class UsuarioTareaForm(forms.ModelForm):
	class Meta:
		model = UsuarioTarea

	def clean_field3(self):
		archivo = self.cleaned_data['archivo']
		#import pdb; pdb.set_trace()
		if archivo.name.split('.')[-1] != 'txt':
			raise forms.ValidationError('Solo se permiten archivos txt')

		return archivo
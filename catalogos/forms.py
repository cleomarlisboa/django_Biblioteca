import datetime
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from catalogos.models import LivroFisico

# class LivroRenovacaoForm(forms.Form):
#     dataRenovacao = forms.DateField(help_text="digite data entre hoje e 4 semanas")

#     def clean_dataRenovacao(self):
#         data = self.cleaned_data['dataRenovacao']
    
#         if data < datetime.date.today():
#             raise ValidationError(_('esta data de renovacao já passou! '))
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('data de renovacao superior a 4 semanas! '))
#         return data
        

class LivroRenovacaoModelForm(ModelForm):

    def clean_dataDevolucao(self):
       data = self.cleaned_data['dataDevolucao']

       if data < datetime.date.today():
           raise ValidationError(_('esta data de renovacao já passou! '))

       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('data de renovacao superior a 4 semanas! '))

       return data

    class Meta:
        model = LivroFisico
        fields = ['dataDevolucao']
        labels = {'dataDevolucao': _('Nova data de devolucao')}
        help_texts = {'dataDevolucao': _('digite data entre hoje e 4 semanas.')}




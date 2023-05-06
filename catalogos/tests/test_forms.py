import datetime
from django.test import TestCase
from django.utils import timezone
from catalogos.forms import LivroRenovacaoModelForm

class LivroRenovacaoFormTest(TestCase):
    def testRenovacaoFormDataCampoLabel(self):
        form = LivroRenovacaoModelForm()
        self.assertTrue(form.fields['dataDevolucao'].label == None or form.fields['dataDevolucao'].label == 'Nova data de devolucao')

    # def testRenovacaoFormDataCampoHelpText(self):
        form = LivroRenovacaoModelForm()
        self.assertEqual(form.fields['dataDevolucao'].help_text, 'digite data entre hoje e 4 semanas.')

    def testRenovacaoFormDataNoPassado(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = LivroRenovacaoModelForm(data={'dataDevolucao': date})
        self.assertFalse(form.is_valid())

    def testRenovacaoFormDataNoFuturo(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = LivroRenovacaoModelForm(data={'dataDevolucao': date})
        self.assertFalse(form.is_valid())

    def testRenovacaoFormDataHoje(self):
        date = datetime.date.today()
        form = LivroRenovacaoModelForm(data={'dataDevolucao': date})
        self.assertTrue(form.is_valid())

    def testRenovacaoFormDataMax(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = LivroRenovacaoModelForm(data={'dataDevolucao': date})
        self.assertTrue(form.is_valid())

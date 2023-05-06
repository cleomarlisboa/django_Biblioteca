from django.test import TestCase
from catalogos.models import Autor


class AutorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Autor.objects.create(nome='Big', sobrenome='Bob')
    
    def testNomeLabel(self):
        autor = Autor.objects.get(id=1)
        campoLabel = autor._meta.get_field('nome').verbose_name
        self.assertEquals(campoLabel,'nome')

    def testDataMorteLabel(self):
        autor = Autor.objects.get(id=1)
        campoLabel = autor._meta.get_field('dataMorte').verbose_name
        self.assertEquals(campoLabel, 'morte')
    
    def testNomeMaxLength(self):
        autor = Autor.objects.get(id=1)
        MaxLength = autor._meta.get_field('nome').max_length
        self.assertEquals(MaxLength,100)

    def testSobrenomeVirgulaNome(self):
        autor = Autor.objects.get(id=1)
        nomeEsperado = f'{autor.nome}, {autor.sobrenome}'
        self.assertEquals(nomeEsperado, str(autor))

    def testGetAbsoluteUrl(self):
        autor = Autor.objects.get(id=1)
        self.assertEquals(autor.get_absolute_url(), '/catalogos/autor/1')

    
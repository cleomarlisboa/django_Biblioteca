from django.test import TestCase
from django.urls import reverse
from catalogos.models import Autor
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from catalogos.models import LivroFisico, Livro, Genero, Idioma


status = 200


class AutorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        autoresQtd = 13

        for autor_id in range(autoresQtd):
            Autor.objects.create(
                nome=f'Machado {autor_id}',
                sobrenome='Assis',
            )

    def testViewUrlExisteCaminhoDesejado(self):
        response = self.client.get('/catalogos/autores')
        self.assertEqual(response.status_code, status)

    def testViewUrlAcessivelNome(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, status)

    def testViewTemplateCorreto(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, status)
        self.assertTemplateUsed(response, 'catalogos/autor_list.html')

    def testPaginacaoDezItens(self):
        response = self.client.get(reverse('autores'))
        self.assertEqual(response.status_code, status)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['autor_list']) == 10)

    def testListarTodosAutores(self):
        response = self.client.get(reverse('autores')+'?page=2')
        self.assertEqual(response.status_code, status)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['autor_list']) == 3)


class EmprestimoPorUsuarioListViewTest(TestCase):
    def setUp(self):

        userTeste1 = User.objects.create_user(username='userTeste1', password='fdsaf564')
        userTeste2 = User.objects.create_user(username='userTeste2', password='dljksaf5462')

        userTeste1.save()
        userTeste2.save()

        autorTeste1 = Autor.objects.create(nome='Manoel', sobrenome='de Barros')
        idiomaTeste1 = Idioma.objects.create(nome='Portugues')
        livroTeste1 = Livro.objects.create(
            titulo='titulo do livro teste 1',
            sumario='sumario livro teste 1',
            isbn='ABCDEFG',
            autor=autorTeste1,
            idioma=idiomaTeste1,
        )

        genero_objects_por_livro = Genero.objects.all()
        livroTeste1.genero.set(genero_objects_por_livro)
        livroTeste1.save()

        livrosCopiasQtd = 30
        for livroCopia in range(livrosCopiasQtd):
            dataDevolucao = timezone.localtime() + datetime.timedelta(days=livroCopia%5)
            mutuario = userTeste1 if livroCopia % 2 else userTeste2
            status = 'm'
            LivroFisico.objects.create(
                livro=livroTeste1,
                publicacao='editora teste, capa dura,  2023',
                dataDevolucao=dataDevolucao,
                mutuario=mutuario,
                status=status,
            )

    def testRedirecionarSeNaoEstiverLogado(self):
        response = self.client.get(reverse('meus-emprestimos'))
        self.assertRedirects(response, '/accounts/login/?next=/catalogos/meusLivros/')

    def testLogadoComTemplateCorreto(self):
        login = self.client.login(username='userTeste1', password='fdsaf564')
        response = self.client.get(reverse('meus-emprestimos'))

        # verificar se usario esta logado
        self.assertEqual(str(response.context['user']), 'userTeste1')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'catalogos/listaMutuarioLivro.html')

    def testSoLivrosEmprestadosNaLista(self):
        login = self.client.login(username='userTeste1', password='fdsaf564')
        response = self.client.get(reverse('meus-emprestimos'))

        self.assertEqual(str(response.context['user']), 'userTeste1')
        self.assertEqual(response.status_code, 200)

        # verificacao inicial de nenhum emprestimo
        self.assertTrue('listaEmprestimos' in response.context)
        self.assertEqual(len(response.context['listaEmprestimos']), 0)

        # colocar todos os livros como emprestado
        livros = LivroFisico.objects.all()[:10]

        for livro in livros:
            livro.status = 'e'
            livro.save()

        # verificacao se há livros emprestados na lista agora
        response = self.client.get(reverse('meus-emprestimos'))
        self.assertEqual(str(response.context['user']), 'userTeste1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('listaEmprestimos' in response.context)

        # verificacao se todos os livros estao emprestados e sao de userTeste1
        for livroitem in response.context['listaEmprestimos']:
            self.assertEqual(response.context['user'], livroitem.mutuario)
            self.assertEqual('e', livroitem.status)

    def testPaginasOrdenadasPorDataDevolucao(self):
        for livro in LivroFisico.objects.all():
            livro.status='e'
            livro.save()

        login = self.client.login(username='userTeste1', password='fdsaf564')
        response = self.client.get(reverse('meus-emprestimos'))

        self.assertEqual(str(response.context['user']), 'userTeste1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['listaEmprestimos']), 10)

        ultimaData = 0
        for livro in response.context['listaEmprestimos']:
            if ultimaData == 0:
                ultimaData = livro.dataDevolucao
            else:
                self.assertTrue(ultimaData <= livro.dataDevolucao)
                ultimaData = livro.dataDevolucao


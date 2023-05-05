from typing import Any
from django.db.models.query import QuerySet
from catalogos.models import Livro, Autor, LivroFisico, Genero
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
#@permission_required('catalogos.verEmprestimos')
def index(request):
    numLivros = Livro.objects.all().count()
    numLivrosFisicos = LivroFisico.objects.all().count()
    numLivrosFisicosDisponiveis = LivroFisico.objects.filter(status__exact='a').count()
    numAutores = Autor.objects.count()

    numVisitas = request.session.get('numVisitas', 1)
    request.session['numVisitas'] = numVisitas + 1

    context = {
        'numLivros': numLivros,
        'numLivrosFisicos': numLivrosFisicos,
        'numLivrosFisicosDisponiveis': numLivrosFisicosDisponiveis,
        'numAutores': numAutores,
        'numVisitas':numVisitas,
    }

    return render(request, 'index.html', context=context)

class LivroListView(LoginRequiredMixin, generic.ListView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    model = Livro
    context_object_name = 'livrosLista'
    # queryset = Livro.objects.filter(titulo__icontains='a')[:5]
    queryset = Livro.objects.all()
    template_name = 'catalogos/livrosLista.html'
    paginate_by = 5

class livroDetalheView(LoginRequiredMixin, generic.DetailView):
    model = Livro

class AutorListView(LoginRequiredMixin, generic.ListView):
    model = Autor
    paginate_by = 1


class autorDetalheView(LoginRequiredMixin, generic.DetailView):
    model = Autor

class EmprestimoPorUsuarioListView(LoginRequiredMixin, generic.ListView):
    model = LivroFisico
    template_name = 'catalogos/listaMutuarioLivro.html'
    paginate_by = 10

    def get_queryset(self):
        return LivroFisico.objects.filter(mutuario=self.request.user).filter(status__exact='e').order_by('dataDevolucao')

class EmprestimosListView(LoginRequiredMixin, generic.ListView):
    model = LivroFisico
    template_name = 'catalogos/listaEmprestimos.html'
    paginate_by = 10
    permission_required = 'catalogos.verEmprestimos'
    
    def get_queryset(self):
        return LivroFisico.objects.filter(status__exact='e').order_by('mutuario')

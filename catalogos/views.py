from typing import Any
from django.db.models.query import QuerySet
from catalogos.models import Livro, Autor, LivroFisico, Genero
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from catalogos.forms import LivroRenovacaoModelForm
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .serializers import LivroSerializer
from rest_framework import viewsets

@login_required
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
    paginate_by = 20

class livroDetalheView(LoginRequiredMixin, generic.DetailView):
    model = Livro

class AutorListView(LoginRequiredMixin, generic.ListView):
    model = Autor
    paginate_by = 10


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
    permission_required = 'catalogos.acessoBibliotecario'
    
    def get_queryset(self):
        return LivroFisico.objects.filter(status__exact='e').order_by('mutuario')


@permission_required("catalogos.acessoBibliotecario")
def bibliotecarioRenovarLivro(request, pk):
    livroFisico = get_object_or_404(LivroFisico, pk=pk)
    if request.method == "POST":
        form = LivroRenovacaoModelForm(request.POST)
        if form.is_valid():
            livroFisico.dataDevolucao = form.cleaned_data['dataDevolucao']
            livroFisico.save()
            return HttpResponseRedirect(reverse('emprestimos'))
    else:
        dataRenovacaoSugerida = datetime.date.today() + datetime.timedelta(weeks=3)
        form = LivroRenovacaoModelForm(initial={'dataDevolucao':dataRenovacaoSugerida})
    
    context = {
        'form':form,
        'livrofisico':livroFisico,
    }
    return render(request, 'catalogos/bibliotecarioRenovarLivro.html', context)

class AutorCriar(LoginRequiredMixin, CreateView):
    model = Autor
    fields = '__all__'
    initial = {'dataMorte':'01/01/2023'}
    permission_required = 'catalogos.acessoBibliotecario'
    

class AutorEditar(LoginRequiredMixin, UpdateView):
    model = Autor
    fields = ['nome', 'sobrenome', 'dataNascimento', 'dataMorte']
    permission_required = 'catalogos.acessoBibliotecario'

class AutorExcluir(LoginRequiredMixin, DeleteView):
    model = Autor
    success_url = reverse_lazy('autores')
    template_name_suffix = '_confirmar_exclusao'
    permission_required = 'catalogos.acessoBibliotecario'


class LivroCriar(LoginRequiredMixin, CreateView):
    permission_required = 'catalogos.acessoBibliotecario'
    model = Livro
    fields = '__all__'

class LivroEditar(LoginRequiredMixin, UpdateView):
    model = Livro
    fields = '__all__'
    permission_required = 'catalogos.acessoBiblioteario'


class LivroExcluir(LoginRequiredMixin, DeleteView):
    model = Livro
    success_url = reverse_lazy('livros')
    permission_required = 'catalogos.acessoBibliotecario'


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer


from django.shortcuts import render
from catalogos.models import Livro, Autor, LivroFisico, Genero
from django.views import generic


def index(request):
    numLivros = Livro.objects.all().count()
    numLivrosFisicos = LivroFisico.objects.all().count()
    numLivrosFisicosDisponiveis = LivroFisico.objects.filter(status__exact='a').count()

    numAutores = Autor.objects.count()

    context = {
        'numLivros': numLivros,
        'numLivrosFisicos': numLivrosFisicos,
        'numLivrosFisicosDisponiveis': numLivrosFisicosDisponiveis,
        'numAutores': numAutores,
    }

    return render(request, 'index.html', context=context)

class LivroListView(generic.ListView):
    model = Livro
    context_object_name = 'livrosLista'
    # queryset = Livro.objects.filter(titulo__icontains='a')[:5]
    queryset = Livro.objects.all()
    template_name = 'catalogos/livrosLista.html'
    paginate_by = 5

class livroDetalheView(generic.DetailView):
    model = Livro

class AutorListView(generic.ListView):
    model = Autor
    paginate_by = 1


class autorDetalheView(generic.DetailView):
    model = Autor

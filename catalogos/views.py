from django.shortcuts import render
from catalogos.models import Livro, Autor, LivroFisico, Genero

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

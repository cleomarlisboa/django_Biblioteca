from django.contrib import admin
from .models import Livro, Autor, Genero, LivroFisico, Idioma

class AutorAdmin(admin.ModelAdmin):
    list_display = ('sobrenome', 'nome', 'dataNascimento', 'dataMorte')
    fields = ['nome', 'sobrenome', ('dataNascimento', 'dataMorte')] # para exibicao nos detalhes do autor, neste caso as 2 datas sao exibidas horizontalmente
    # atributo exclude para excluir da exibição

class LivroFisicoInline(admin.TabularInline):
    model = LivroFisico
    extra = 0

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    inlines = [LivroFisicoInline] # no detalhamento de um livro exibe na parte final info de livros fisicos relacionados ao livro
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.TabularInline

@admin.register(LivroFisico)
class LivroFisicoAdmin(admin.ModelAdmin):
    #list_display = ('livro', 'status', 'mutuario', 'dataDevolucao', 'id)
    list_filter = ('status', 'dataDevolucao')

    fieldsets = (
        (None, {
            'fields': ('livro', 'publicacao', 'id')
        }),
        ('Disponibilidade', {
            'fields': ('status', 'dataDevolucao', 'mutuario')
        }),
        )




# admin.site.register(Livro)
#admin.site.register(Autor)
admin.site.register(Genero)
# admin.site.register(LivroFisico)
admin.site.register(Idioma)
admin.site.register(Autor, AutorAdmin)
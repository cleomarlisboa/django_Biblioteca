from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class meuModelo(models.Model):

    meuCampo = models.CharField(max_length=20, help_text='digite meuCampo')

    class Meta:
        ordering = ['-meuCampo']

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

class Genero(models.Model):
    nome = models.CharField(max_length=200, help_text='digite um genero de livro')

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Titulo do livro"    )

    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)

    sumario = models.TextField(max_length=1000, help_text='digite uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genero = models.ManyToManyField(Genero, help_text='selecione o(s) genero(s) do livro')
    idioma = models.ForeignKey('Idioma', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('livro-detalhe', args=[str(self.id)])
    
    def display_genero(self):
        return ', '.join(genero.nome for genero in self.genero.all()[:3])

    display_genero.short_description = 'Genero'
    

class LivroFisico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para este livro específico.')
    livro = models.ForeignKey('Livro', on_delete=models.SET_NULL, null=True)
    publicacao = models.CharField(max_length=200)
    dataDevolucao= models.DateField(null=True, blank=True)
    mutuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    SituacaoEmprestimo = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=SituacaoEmprestimo,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro:',
    )

    class Meta:
        ordering = ['dataDevolucao']
        permissions = (("fazerDevolucao", "definir livro como devolvido"),("verEmprestimos"," ver todos os emprestimos"))

    def __str__(self):
        return f'{self.id} ({self.livro.titulo})'
    
    @property
    def esta_atrasado(self):
        if self.dataDevolucao and date.today() > self.dataDevolucao:
            return True
        return False


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    dataNascimento = models.DateField(null=True, blank=True)
    dataMorte = models.DateField('Morto', null=True, blank=True)

    class Meta:
        ordering = ['nome', 'sobrenome']

    def get_absolute_url(self):
        return reverse('autor-detalhe', args=[str(self.id)])

    def __str__(self):
        return f'{self.nome}, {self.sobrenome}'

class Idioma(models.Model):
    nome = models.CharField(max_length=200,
                            help_text="digite o idioma do livro")

    def __str__(self):
        return self.nome
    
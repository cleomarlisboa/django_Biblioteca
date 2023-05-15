from django.urls import path
from catalogos import views


urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.LivroListView.as_view(), name='livros'),
    path('livro/<int:pk>', views.livroDetalheView.as_view(), name='livro-detalhe'),
    path('autores/', views.AutorListView.as_view(), name='autores'),
    path('autor/<int:pk>', views.autorDetalheView.as_view(), name='autor-detalhe'),
]

urlpatterns += [
    path('meusLivros/', views.EmprestimoPorUsuarioListView.as_view(), name='meus-emprestimos'),
    path('emprestimos/', views.EmprestimosListView.as_view(), name='emprestimos'),
]

urlpatterns += [
    path('livro/<uuid:pk>/renovar/', views.bibliotecarioRenovarLivro, name='bibliotecarioRenovarLivro'),
]

urlpatterns += [
    path('autor/criar/', views.AutorCriar.as_view(), name='autorCriar'),
    path('autor/<int:pk>/editar/', views.AutorEditar.as_view(), name='autorEditar'),
    path('autor/<int:pk>/excluir/', views.AutorExcluir.as_view(), name='autorExcluir'),
]


urlpatterns += [
    path('livro/criar/', views.LivroCriar.as_view(), name='livroCriar' ),
    path('livro/<int:pk>/editar/', views.LivroEditar.as_view(), name='livroEditar'),
    path('livro/<int:pk>/excluir/', views.LivroExcluir.as_view(), name='livroExcluir'),
    
]

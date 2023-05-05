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

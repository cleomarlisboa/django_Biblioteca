from django.urls import path
from catalogos import views

urlpatterns = [
    path('', views.index, name='index'),
]


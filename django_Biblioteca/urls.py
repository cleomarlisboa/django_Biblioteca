from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from catalogos.views import LivroViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalogos/', include('catalogos.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/catalogos/')),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]



router = routers.DefaultRouter()
router.register(r'livrosAPI', LivroViewSet)

urlpatterns += [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
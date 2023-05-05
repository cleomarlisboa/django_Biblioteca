from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

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
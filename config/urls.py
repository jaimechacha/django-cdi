"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0.3/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings as setting
from core.dashboard.views import *
from core.iniciopage.views import *


urlpatterns = [
    #path('', IndexView.as_view(), name="inicio"),
    #path('inicio', IndexView.as_view(), name="inicio"),
    path('', pagina, name="inicio"),
    path('inicio', pagina, name="inicio"),

    path('web/update/', WebUpdateView.as_view(), name='web'),
    path('web/update/<int:pk>', ActualizarWeb.as_view(), name='web'),
    #path('suscripcion/', SuscripcionView.as_view(), name='suscripcion'),
    path('suscripcion/', Suscripcion, name='suscripcion'),
    path('contacto/', ContactoView.as_view(), name='contacto'),

    #path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('security/', include('core.security.urls')),
    path('login/', include('core.login.urls')),
    path('user/', include('core.user.urls')),
    path('school/', include('core.school.urls')),
    path('inventory/', include('core.inventory.urls')),
    path('reports/', include('core.reports.urls')),
]

if setting.DEBUG:
    urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)

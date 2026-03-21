"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from routes.home import All_Routes
from routes.alert_route import alert


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cadastro/', All_Routes['Login']['cadastro'], name='cadastro'),
    path('api/login/', All_Routes['Login']['login'], name='login'),
    path('api/usuarios/', All_Routes['Consulta']['usuarios'], name='usuarios'),
    path('api/doctors/cadastro/', All_Routes['Doctor']['cadastro'], name='doctor_cadastro'),
    path('api/doctors/', All_Routes['Doctor']['lista'], name='doctor_lista'),
    path('api/doctors/<int:doctor_id>/', All_Routes['Doctor']['detalhe'], name='doctor_detalhe'),
    path('api/instituicoes/cadastro/', All_Routes['Instituicao']['cadastro'], name='instituicao_cadastro'),
    path('api/instituicoes/', All_Routes['Instituicao']['lista'], name='instituicao_lista'),
    path('api/instituicoes/<int:id_doctor>/', All_Routes['Instituicao']['detalhe'], name='instituicao_detalhe'),
    path('api/cuidadores/cadastro/', All_Routes['Cuidador']['cadastro'], name='cuidador_cadastro'),
    path('api/cuidadores/', All_Routes['Cuidador']['lista'], name='cuidador_lista'),
    path('api/cuidadores/<int:cuidador_id>/', All_Routes['Cuidador']['detalhe'], name='cuidador_detalhe'),
    path('api/cuidadores/<int:cuidador_id>/idoso/', All_Routes['Cuidador']['detalhe_idoso'], name='cuidador_idoso'),
    path('api/idosos/cadastro/', All_Routes['Idoso']['cadastro'], name='idoso_cadastro'),
    path('api/alert/', alert, name='alert'),
]

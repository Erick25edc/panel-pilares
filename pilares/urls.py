from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mapa/', views.mapa, name='mapa'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('reporte-pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
    path('api/pilares/<str:clave_id>/editar/', views.editar_pilares, name='editar_pilares'),
    path('api/equipo/agregar/', views.agregar_equipo_no_funcional, name='agregar_equipo'),
    path('api/equipo/<int:equipo_id>/editar/', views.editar_equipo_no_funcional, name='editar_equipo'),
]
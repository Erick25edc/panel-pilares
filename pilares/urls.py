from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mapa/', views.mapa, name='mapa'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('historial/', views.historial_general, name='historial_general'),
    path('incidencias/', views.incidencias, name='incidencias'),
    path('reporte-pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
    path('api/pilares/<str:clave_id>/editar/', views.editar_pilares, name='editar_pilares'),
    path('api/pilares/<str:clave_id>/incidencias/', views.api_incidencias_pilares, name='api_incidencias_pilares'),
    path('api/incidencia/crear/', views.crear_incidencia, name='crear_incidencia'),
    path('api/incidencia/<int:incidencia_id>/actualizar/', views.actualizar_incidencia, name='actualizar_incidencia'),
    path('api/equipo/agregar/', views.agregar_equipo_no_funcional, name='agregar_equipo'),
    path('api/equipo/<int:equipo_id>/editar/', views.editar_equipo_no_funcional, name='editar_equipo'),
    path('reporte-incidencias-general-pdf/', views.reporte_incidencias_general_pdf, name='reporte_incidencias_general_pdf'),
    path('reporte-incidencias-general-excel/', views.reporte_incidencias_general_excel, name='reporte_incidencias_general_excel'),
    path('api/equipos-detalle/<str:clave_id>/', views.api_equipos_detalle, name='api_equipos_detalle'),
    path('api/equipo-detalle/agregar/', views.agregar_equipo_detalle, name='agregar_equipo_detalle'),
    path('api/equipo-detalle/<int:equipo_id>/editar/', views.editar_equipo_detalle, name='editar_equipo_detalle'),
    path('api/equipo-detalle/<int:equipo_id>/eliminar/', views.eliminar_equipo_detalle, name='eliminar_equipo_detalle'),
    path('api/equipo-detalle/importar-csv/', views.importar_csv_equipos, name='importar_csv_equipos'),
    # 🔥 NUEVA RUTA: Exportar todos los equipos
    path('exportar-todos-equipos-excel/', views.exportar_todos_equipos_excel, name='exportar_todos_equipos_excel'),
]

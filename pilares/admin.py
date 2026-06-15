from django.contrib import admin
from .models import Pilares, EquipoNoFuncional

# ============ ADMIN PARA PILARES ============
@admin.register(Pilares)
class PilaresAdmin(admin.ModelAdmin):
    list_display = ('clave_id', 'nombre', 'alcaldia', 'modelo_equipo', 'pasta_termica', 'mouse_nuevos', 'teclados_nuevos', 'equipos_8gb', 'total_equipos', 'equipos_inactivos', 'fecha_mantenimiento')
    list_filter = ('alcaldia',)
    search_fields = ('clave_id', 'nombre', 'alcaldia', 'modelo_equipo')
    list_editable = ('modelo_equipo', 'pasta_termica', 'mouse_nuevos', 'teclados_nuevos', 'equipos_8gb', 'total_equipos', 'fecha_mantenimiento')
    list_per_page = 25

# ============ ADMIN PARA EQUIPOS NO FUNCIONALES ============
@admin.register(EquipoNoFuncional)
class EquipoNoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'pilares', 'equipo', 'tipo_falla', 'estado', 'fecha_reporte')
    list_filter = ('tipo_falla', 'estado', 'fecha_reporte')
    search_fields = ('equipo', 'pilares__nombre', 'pilares__clave_id')
    list_editable = ('estado',)  # Permite editar el estado directamente desde la lista
    list_per_page = 25
    date_hierarchy = 'fecha_reporte'  # Navegación por fechas

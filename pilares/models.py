from django.db import models

class Pilares(models.Model):
    """Modelo para los PILARES de CDMX"""
    
    # Identificación
    clave_id = models.CharField('Clave ID', max_length=50, unique=True, primary_key=True)
    nombre = models.CharField('Nombre del PILARES', max_length=200)
    alcaldia = models.CharField('Alcaldía', max_length=100)
    
    # Dirección
    calle = models.CharField('Calle', max_length=200, blank=True)
    codigo_postal = models.CharField('Código Postal', max_length=10, blank=True)
    colonia = models.CharField('Colonia', max_length=200, blank=True)
    # 🔥 NUEVO CAMPO 🔥
    modelo_equipo = models.CharField('Modelo del equipo', max_length=100, blank=True, default='')
    
    # Coordenadas (¡importantes para el mapa!)
    latitud = models.DecimalField('Latitud', max_digits=10, decimal_places=6)
    longitud = models.DecimalField('Longitud', max_digits=10, decimal_places=6)
    
    # Datos de mantenimiento
    pasta_termica = models.IntegerField('% Pasta térmica', default=0)
    mouse_nuevos = models.IntegerField('Mouse nuevos', default=0)
    teclados_nuevos = models.IntegerField('Teclados nuevos', default=0)
    equipos_8gb = models.IntegerField('Equipos con 8GB RAM', default=0)
    total_equipos = models.IntegerField('Total equipos', default=0)
    
    fecha_mantenimiento = models.DateField('Fecha último mantenimiento', null=True, blank=True)
    observaciones = models.TextField('Observaciones', blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def porcentaje_8gb(self):
        """Calcula el porcentaje de equipos con 8GB RAM"""
        if self.total_equipos > 0:
            return round((self.equipos_8gb / self.total_equipos) * 100, 1)
        return 0
    
    @property
    def zona(self):
        """Determina la zona según el prefijo de CLAVE_ID"""
        if '_' in self.clave_id:
            partes = self.clave_id.split('_')
            if len(partes) >= 2:
                prefijo = partes[1]
                zonas = {
                    'NT': 'NORTE', 'PT': 'PONIENTE', 'CO': 'CENTRO',
                    'IZ': 'ORIENTE', 'SU': 'SUR', 'SP': 'SUR PONIENTE'
                }
                return zonas.get(prefijo, 'SIN ZONA')
        return 'SIN ZONA'
    
    def __str__(self):
        return f"{self.clave_id} - {self.nombre}"
    
    class Meta:
        verbose_name = 'PILARES'
        verbose_name_plural = 'PILARES'
        ordering = ['nombre']
class EquipoNoFuncional(models.Model):
    """Modelo para seguimiento de equipos no funcionales"""
    
    TIPO_FALLA = [
        ('MOTHER', 'Placa Madre (Motherboard)'),
        ('VIDEO', 'Tarjeta de Video'),
        ('RAM', 'Memoria RAM'),
        ('DISCO', 'Disco Duro/SSD'),
        ('FUENTE', 'Fuente de Poder'),
        ('PANTALLA', 'Pantalla'),
        ('TECLADO', 'Teclado'),
        ('MOUSE', 'Mouse'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADO = [
        ('PENDIENTE', 'Pendiente de revisión'),
        ('REPARADO', 'Reparado'),
        ('DESECHADO', 'Desechado'),
        ('EN_GARANTIA', 'En garantía'),
    ]
    
    # Relación con PILARES
    pilares = models.ForeignKey('Pilares', on_delete=models.CASCADE, related_name='equipos_no_funcionales')
    
    # Datos del equipo
    equipo = models.CharField('Nombre/Modelo del equipo', max_length=100)
    tipo_falla = models.CharField('Tipo de falla', max_length=20, choices=TIPO_FALLA)
    descripcion = models.TextField('Descripción de la falla', blank=True)
    
    # Periféricos
    mouse = models.BooleanField('Mouse no funcional', default=False)
    teclado = models.BooleanField('Teclado no funcional', default=False)
    monitor = models.BooleanField('Monitor no funcional', default=False)
    
    # Estado y seguimiento
    estado = models.CharField('Estado', max_length=20, choices=ESTADO, default='PENDIENTE')
    fecha_reporte = models.DateField('Fecha de reporte', auto_now_add=True)
    fecha_solucion = models.DateField('Fecha de solución', null=True, blank=True)
    observaciones = models.TextField('Observaciones adicionales', blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.pilares.nombre} - {self.equipo} ({self.get_tipo_falla_display()})"
    
    class Meta:
        verbose_name = 'Equipo no funcional'
        verbose_name_plural = 'Equipos no funcionales'
        ordering = ['-fecha_reporte']

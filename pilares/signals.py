from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pilares, ObservacionHistorial

@receiver(post_save, sender=Pilares)
def guardar_historial_observacion(sender, instance, created, **kwargs):
    if created:
        ObservacionHistorial.objects.create(
            pilares=instance,
            observacion_nueva=instance.observaciones or 'Sin observaciones',
            tipo_cambio='CREACION',
        )
    else:
        try:
            old_instance = Pilares.objects.get(pk=instance.pk)
            if old_instance.observaciones != instance.observaciones:
                ObservacionHistorial.objects.create(
                    pilares=instance,
                    observacion_anterior=old_instance.observaciones or '',
                    observacion_nueva=instance.observaciones or '',
                    tipo_cambio='ACTUALIZACION',
                )
        except Pilares.DoesNotExist:
            pass
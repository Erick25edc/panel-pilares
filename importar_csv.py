# importar_pilares_csv.py
import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pilares.models import Pilares

# Ruta del archivo CSV
archivo = 'PILARES.csv'

# Leer el CSV
with open(archivo, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("Columnas encontradas:", reader.fieldnames)
    
    for row in reader:
        try:
            # Crear o actualizar el registro
            pilares, created = Pilares.objects.get_or_create(
                clave_id=row['clave_id'],
                defaults={
                    'nombre': row.get('nombre', ''),
                    'alcaldia': row.get('alcaldia', ''),
                    'calle': row.get('calle', ''),
                    'codigo_postal': row.get('codigo_postal', ''),
                    'colonia': row.get('colonia', ''),
                    'modelo_equipo': row.get('modelo_equipo', ''),
                    'latitud': float(row.get('latitud', 0)),
                    'longitud': float(row.get('longitud', 0)),
                    'pasta_termica': int(row.get('pasta_termica', 0)),
                    'mouse_nuevos': int(row.get('mouse_nuevos', 0)),
                    'teclados_nuevos': int(row.get('teclados_nuevos', 0)),
                    'equipos_8gb': int(row.get('equipos_8gb', 0)),
                    'total_equipos': int(row.get('total_equipos', 0)),
                    'equipos_inactivos': int(row.get('equipos_inactivos', 0)),
                    'observaciones': row.get('observaciones', ''),
                }
            )
            if created:
                print(f"✅ Creado: {pilares.nombre}")
            else:
                print(f"🔄 Actualizado: {pilares.nombre}")
        except Exception as e:
            print(f"❌ Error en fila: {e}")
            print(f"Datos: {row}")

print("¡Importación completada!")

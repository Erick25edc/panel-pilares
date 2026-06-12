import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pilares.models import Pilares

def detectar_codificacion(ruta_archivo):
    """Detecta la codificación del archivo"""
    import chardet
    with open(ruta_archivo, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def importar_csv(ruta_archivo):
    """Importa datos desde un CSV a la base de datos"""
    
    # Detectar codificación automáticamente
    try:
        import chardet
        with open(ruta_archivo, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            print(f"📄 Codificación detectada: {encoding}")
    except:
        # Si no está instalado chardet, probar codificaciones comunes
        encoding = None
    
    # Probar diferentes codificaciones
    codificaciones = [encoding, 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1'] if encoding else ['utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    creados = 0
    actualizados = 0
    errores = 0
    
    for codif in codificaciones:
        if codif is None:
            continue
        try:
            print(f"🔍 Probando codificación: {codif}")
            with open(ruta_archivo, 'r', encoding=codif) as file:
                reader = csv.DictReader(file)
                
                # Mostrar columnas encontradas
                print(f"📋 Columnas encontradas: {list(reader.fieldnames) if reader.fieldnames else 'No se encontraron'}")
                
                for row in reader:
                    try:
                        # Buscar si ya existe
                        clave_id = row.get('CLAVE_ID', '').strip()
                        if not clave_id:
                            continue
                        
                        obj, created = Pilares.objects.update_or_create(
                            clave_id=clave_id,
                            defaults={
                                'nombre': row.get('PILARES', '') or row.get('Nombre', '') or '',
                                'alcaldia': row.get('ALCALDIA', '') or row.get('Alcaldía', '') or '',
                                'calle': row.get('CALLE', '') or row.get('Calle', '') or '',
                                'codigo_postal': row.get('CÓDIGO POSTAL', '') or row.get('Codigo Postal', '') or '',
                                'colonia': row.get('COLONIA', '') or row.get('Colonia', '') or '',
                                'latitud': float(row.get('Latitud_Y', 0) or row.get('Latitud', 0) or 0),
                                'longitud': float(row.get('Longitud_X', 0) or row.get('Longitud', 0) or 0),
                                'pasta_termica': int(float(row.get('% PASTA TÉRMICA', 0) or row.get('Pasta Termica', 0) or 0)),
                                'mouse_nuevos': int(float(row.get('MOUSE NUEVOS', 0) or row.get('Mouse Nuevos', 0) or 0)),
                                'teclados_nuevos': int(float(row.get('TECLADOS NUEVOS', 0) or row.get('Teclados Nuevos', 0) or 0)),
                                'equipos_8gb': int(float(row.get('EQUIPOS 8GB RAM', 0) or row.get('Equipos 8GB', 0) or 0)),
                                'total_equipos': int(float(row.get('TOTAL EQUIPOS', 0) or row.get('Total Equipos', 0) or 0)),
                                'observaciones': row.get('OBSERVACIONES', '') or row.get('Observaciones', '') or '',
                            }
                        )
                        
                        # Importar fecha si existe
                        fecha_str = row.get('FECHA_ULT_MANTENIMIENTO', '') or row.get('Fecha Mantenimiento', '')
                        if fecha_str and fecha_str.strip():
                            from datetime import datetime
                            try:
                                # Probar diferentes formatos de fecha
                                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']:
                                    try:
                                        obj.fecha_mantenimiento = datetime.strptime(fecha_str.strip(), fmt).date()
                                        obj.save()
                                        break
                                    except:
                                        continue
                            except:
                                pass
                        
                        if created:
                            creados += 1
                            print(f"✓ Creado: {obj.clave_id} - {obj.nombre}")
                        else:
                            actualizados += 1
                            print(f"↻ Actualizado: {obj.clave_id} - {obj.nombre}")
                        
                    except Exception as e:
                        errores += 1
                        print(f"✗ Error en fila: {row.get('CLAVE_ID', '?')} - {str(e)}")
                
                # Si llegamos aquí, la codificación funcionó
                print(f"\n✅ Importación exitosa con codificación: {codif}")
                break
                
        except UnicodeDecodeError:
            print(f"❌ Falló con codificación: {codif}")
            continue
        except Exception as e:
            print(f"❌ Error general con {codif}: {str(e)}")
            continue
    
    print(f"\n{'='*50}")
    print(f"📊 Resumen de importación:")
    print(f"  ✅ Creados: {creados}")
    print(f"  🔄 Actualizados: {actualizados}")
    print(f"  ❌ Errores: {errores}")
    print(f"{'='*50}")

if __name__ == '__main__':
    # Cambia por la ruta de tu archivo CSV
    importar_csv('pilares.csv')
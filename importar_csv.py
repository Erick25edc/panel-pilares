# importar_pilares_csv.py
import csv
import os
import django
import re

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pilares.models import Pilares

def extraer_numero(texto):
    """Extrae el número de un string como '10 / 26' o '0%'"""
    if not texto or texto == '':
        return 0
    
    # Convertir a string por si acaso
    texto = str(texto).strip()
    
    # Buscar el primer número en el texto
    numeros = re.findall(r'\d+', texto)
    if numeros:
        return int(numeros[0])
    return 0

def importar_csv(archivo='PILARES.csv'):
    """Importa datos desde PILARES.csv a la tabla Pilares"""
    
    print(f"📂 Leyendo archivo: {archivo}")
    
    try:
        with open(archivo, 'r', encoding='utf-8-sig') as f:  # utf-8-sig elimina el BOM
            reader = csv.DictReader(f)
            
            print("\n📋 Columnas encontradas:")
            for col in reader.fieldnames:
                print(f"  - {col}")
            
            print("\n🔄 Iniciando importación...\n")
            
            creados = 0
            actualizados = 0
            errores = 0
            
            for row_num, row in enumerate(reader, 2):  # empezar en 2 por el encabezado
                try:
                    # Limpiar y validar datos
                    clave_id = row.get('CLAVE_ID', '').strip()
                    if not clave_id:
                        print(f"⚠️ Fila {row_num}: Sin CLAVE_ID, saltando")
                        errores += 1
                        continue
                    
                    # Extraer valores numéricos de strings
                    equipos_8gb = extraer_numero(row.get('EQUIPOS 8GB', '0'))
                    inactivos = extraer_numero(row.get('INACTIVOS', '0'))
                    pasta = extraer_numero(row.get('% PASTA', '0%'))
                    mouse = extraer_numero(row.get('MOUSE', '0'))
                    teclados = extraer_numero(row.get('TECLADOS', '0'))
                    
                    # Obtener zona del CLAVE_ID (automático)
                    zona = 'SIN ZONA'
                    if '_' in clave_id:
                        partes = clave_id.split('_')
                        if len(partes) >= 2:
                            prefijo = partes[1].upper()
                            zonas = {
                                'NT': 'NORTE', 'PT': 'PONIENTE', 'CO': 'CENTRO',
                                'IZ': 'ORIENTE', 'SU': 'SUR', 'SP': 'SUR PONIENTE'
                            }
                            zona = zonas.get(prefijo, 'SIN ZONA')
                    
                    # Buscar si ya existe o crear nuevo
                    pilares, created = Pilares.objects.get_or_create(
                        clave_id=clave_id,
                        defaults={
                            'nombre': row.get('PILARES', '').strip(),
                            'alcaldia': row.get('ALCALDIA', '').strip(),
                            'modelo_equipo': row.get('MODELO', '').strip(),
                            'equipos_8gb': equipos_8gb,
                            'equipos_inactivos': inactivos,
                            'pasta_termica': pasta,
                            'mouse_nuevos': mouse,
                            'teclados_nuevos': teclados,
                            # Valores por defecto (si no están en el CSV)
                            'total_equipos': equipos_8gb + inactivos,  # Total = 8GB + Inactivos
                            'calle': '',
                            'codigo_postal': '',
                            'colonia': '',
                            'latitud': 0.0,
                            'longitud': 0.0,
                            'observaciones': f"Zona: {zona}",
                        }
                    )
                    
                    # Si ya existía, actualizar campos
                    if not created:
                        pilares.nombre = row.get('PILARES', '').strip()
                        pilares.alcaldia = row.get('ALCALDIA', '').strip()
                        pilares.modelo_equipo = row.get('MODELO', '').strip()
                        pilares.equipos_8gb = equipos_8gb
                        pilares.equipos_inactivos = inactivos
                        pilares.pasta_termica = pasta
                        pilares.mouse_nuevos = mouse
                        pilares.teclados_nuevos = teclados
                        pilares.total_equipos = equipos_8gb + inactivos
                        pilares.observaciones = f"Zona: {zona}"
                        pilares.save()
                        
                        actualizados += 1
                        print(f"🔄 Actualizado: {clave_id} - {pilares.nombre}")
                    else:
                        creados += 1
                        print(f"✅ Creado: {clave_id} - {pilares.nombre}")
                        
                except Exception as e:
                    errores += 1
                    print(f"❌ Error en fila {row_num}: {row.get('CLAVE_ID', '')} - {str(e)}")
            
            # Resumen final
            print("\n" + "="*50)
            print("📊 RESUMEN DE IMPORTACIÓN")
            print("="*50)
            print(f"✅ Creados: {creados}")
            print(f"🔄 Actualizados: {actualizados}")
            print(f"❌ Errores: {errores}")
            print(f"📝 Total procesados: {creados + actualizados + errores}")
            print("="*50)
            
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo}'")
        print("Asegúrate de que el archivo esté en el directorio actual")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    importar_csv()

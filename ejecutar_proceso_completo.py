#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Principal para Ejecutar el Proceso ETL Completo
Kaggle Survey 2019 - Ingeniería de Sistemas

Este script ejecuta todo el proceso ETL, análisis y validación
"""

import os
import sys
import subprocess
from datetime import datetime

def ejecutar_script(script_name, description):
    """
    Ejecuta un script de Python y maneja errores
    
    Args:
        script_name (str): Nombre del script a ejecutar
        description (str): Descripción del script
    """
    print(f"\n{'='*60}")
    print(f"🚀 EJECUTANDO: {description}")
    print(f"📄 Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Ejecutar el script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ {description} completado exitosamente")
            if result.stdout:
                print("📋 Salida del script:")
                print(result.stdout)
        else:
            print(f"❌ Error en {description}")
            print(f"📋 Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error al ejecutar {script_name}: {str(e)}")
        return False
    
    return True

def verificar_archivos_requeridos():
    """
    Verifica que los archivos requeridos existan
    """
    print("🔍 VERIFICANDO ARCHIVOS REQUERIDOS")
    print("-" * 40)
    
    archivos_requeridos = [
        "multipleChoiceResponses.csv",
        "etl_kaggle_survey.py",
        "analisis_visualizaciones.py",
        "comparacion_powerbi.py"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"\n❌ ERROR: Faltan los siguientes archivos:")
        for archivo in archivos_faltantes:
            print(f"   • {archivo}")
        return False
    
    print("\n✅ Todos los archivos requeridos están presentes")
    return True

def instalar_dependencias():
    """
    Instala las dependencias requeridas
    """
    print("\n📦 INSTALANDO DEPENDENCIAS")
    print("-" * 30)
    
    dependencias = [
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "plotly",
        "openpyxl"
    ]
    
    for dep in dependencias:
        try:
            print(f"📦 Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"⚠️  {dep} ya está instalado o hubo un problema")
    
    print("✅ Instalación de dependencias completada")

def mostrar_resumen_final():
    """
    Muestra un resumen de los archivos generados
    """
    print("\n" + "="*80)
    print("📊 RESUMEN DE ARCHIVOS GENERADOS")
    print("="*80)
    
    # Buscar archivos generados
    archivos_generados = []
    
    # Archivos CSV
    csv_files = [f for f in os.listdir('.') if f.startswith('kaggle_survey_cleaned_') and f.endswith('.csv')]
    archivos_generados.extend(csv_files)
    
    # Archivos Excel
    excel_files = [f for f in os.listdir('.') if f.startswith('kaggle_survey_cleaned_') and f.endswith('.xlsx')]
    archivos_generados.extend(excel_files)
    
    # Archivos de metadatos
    metadata_files = [f for f in os.listdir('.') if f.startswith('metadata_etl_') and f.endswith('.txt')]
    archivos_generados.extend(metadata_files)
    
    # Archivos de visualización
    viz_files = [f for f in os.listdir('.') if f.startswith('analisis_') and f.endswith('.png')]
    archivos_generados.extend(viz_files)
    
    # Archivos de Power BI
    powerbi_files = [f for f in os.listdir('.') if 'powerbi' in f.lower() and f.endswith('.txt')]
    archivos_generados.extend(powerbi_files)
    
    # Archivos de resumen
    summary_files = [f for f in os.listdir('.') if f.startswith('resumen_') and f.endswith('.txt')]
    archivos_generados.extend(summary_files)
    
    if archivos_generados:
        print("📁 ARCHIVOS GENERADOS:")
        for archivo in sorted(archivos_generados):
            tamaño = os.path.getsize(archivo) / 1024  # KB
            print(f"   • {archivo} ({tamaño:.1f} KB)")
    else:
        print("⚠️  No se encontraron archivos generados")
    
    print(f"\n📊 TOTAL DE ARCHIVOS: {len(archivos_generados)}")
    
    # Mostrar instrucciones finales
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Revisar el informe detallado: INFORME_ETL_KAGGLE_SURVEY.md")
    print("2. Abrir Power BI Desktop y ejecutar el script generado")
    print("3. Comparar resultados con las métricas de validación")
    print("4. Crear dashboard siguiendo las instrucciones")
    print("5. Utilizar los insights para decisiones tecnológicas")

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    print("🚀 PROCESO ETL COMPLETO - KAGGLE SURVEY 2019")
    print("🎯 Aplicación: Ingeniería de Sistemas")
    print("="*80)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar archivos requeridos
    if not verificar_archivos_requeridos():
        print("\n❌ ERROR: No se pueden ejecutar los scripts sin los archivos requeridos")
        return False
    
    # Instalar dependencias
    instalar_dependencias()
    
    # Ejecutar proceso ETL
    if not ejecutar_script("etl_kaggle_survey.py", "Proceso ETL Completo"):
        print("\n❌ ERROR: Falló el proceso ETL")
        return False
    
    # Ejecutar análisis y visualizaciones
    if not ejecutar_script("analisis_visualizaciones.py", "Análisis y Visualizaciones"):
        print("\n⚠️  ADVERTENCIA: Falló el análisis de visualizaciones")
        print("   Continuando con la validación de Power BI...")
    
    # Ejecutar comparación con Power BI
    if not ejecutar_script("comparacion_powerbi.py", "Comparación con Power BI"):
        print("\n⚠️  ADVERTENCIA: Falló la comparación con Power BI")
    
    # Mostrar resumen final
    mostrar_resumen_final()
    
    print(f"\n⏰ Finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print("📊 El dataset está listo para análisis en Power BI")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Proceso completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Proceso falló")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)

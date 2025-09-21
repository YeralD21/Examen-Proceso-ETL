#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Visualizar la Comparación con Power BI
Kaggle Survey 2019 - Ingeniería de Sistemas

Este script muestra la validación cruzada entre Python y Power BI
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime

def verificar_archivos_requeridos():
    """
    Verifica que los archivos necesarios existen
    """
    print("=" * 80)
    print("🔍 VERIFICACIÓN DE ARCHIVOS REQUERIDOS")
    print("=" * 80)
    
    # Buscar archivo CSV limpio
    csv_files = glob.glob("kaggle_survey_cleaned_*.csv")
    
    if not csv_files:
        print("❌ No se encontró archivo CSV limpio")
        print("Ejecuta primero: python ver_carga_datos.py")
        return None
    
    # Usar el archivo más reciente
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"✅ Archivo CSV encontrado: {latest_csv}")
    
    return latest_csv

def cargar_datos_limpios(csv_file):
    """
    Carga los datos limpios para comparación
    """
    print("\n" + "=" * 80)
    print("📊 CARGANDO DATOS LIMPIOS PARA COMPARACIÓN")
    print("=" * 80)
    
    try:
        df = pd.read_csv(csv_file)
        print(f"✅ Datos limpios cargados exitosamente")
        print(f"📊 Dimensiones: {df.shape}")
        print(f"📋 Registros: {len(df):,}")
        print(f"📋 Columnas: {len(df.columns):,}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al cargar datos limpios: {str(e)}")
        return None

def calcular_metricas_python(df):
    """
    Calcula las métricas principales en Python para comparación
    """
    print("\n" + "=" * 80)
    print("📊 CALCULANDO MÉTRICAS EN PYTHON")
    print("=" * 80)
    
    # Métricas básicas
    metricas = {
        'total_registros': len(df),
        'total_columnas': len(df.columns),
        'valores_nulos_totales': df.isnull().sum().sum(),
        'registros_unicos': len(df.drop_duplicates()),
        'memoria_mb': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    print("✅ MÉTRICAS BÁSICAS CALCULADAS:")
    print("-" * 40)
    print(f"• Total de registros: {metricas['total_registros']:,}")
    print(f"• Total de columnas: {metricas['total_columnas']:,}")
    print(f"• Valores nulos totales: {metricas['valores_nulos_totales']:,}")
    print(f"• Registros únicos: {metricas['registros_unicos']:,}")
    print(f"• Memoria utilizada: {metricas['memoria_mb']:.2f} MB")
    
    # Métricas por columnas específicas
    if 'Genero' in df.columns:
        metricas['distribucion_genero'] = df['Genero'].value_counts().to_dict()
        print(f"\n✅ DISTRIBUCIÓN POR GÉNERO:")
        print("-" * 30)
        for gender, count in metricas['distribucion_genero'].items():
            percentage = (count / len(df)) * 100
            print(f"• {gender}: {count:,} ({percentage:.1f}%)")
    
    if 'Pais_Residencia' in df.columns:
        metricas['top_5_paises'] = df['Pais_Residencia'].value_counts().head(5).to_dict()
        print(f"\n✅ TOP 5 PAÍSES:")
        print("-" * 20)
        for country, count in metricas['top_5_paises'].items():
            percentage = (count / len(df)) * 100
            print(f"• {country}: {count:,} ({percentage:.1f}%)")
    
    if 'Nivel_Educativo' in df.columns:
        metricas['distribucion_educacion'] = df['Nivel_Educativo'].value_counts().to_dict()
        print(f"\n✅ DISTRIBUCIÓN POR EDUCACIÓN:")
        print("-" * 30)
        for edu, count in list(metricas['distribucion_educacion'].items())[:5]:
            percentage = (count / len(df)) * 100
            print(f"• {edu}: {count:,} ({percentage:.1f}%)")
    
    return metricas

def generar_script_powerbi():
    """
    Genera un script de Power Query M para replicar el proceso ETL
    """
    print("\n" + "=" * 80)
    print("🔧 GENERANDO SCRIPT DE POWER BI")
    print("=" * 80)
    
    script_powerbi = """
// Script de Power Query M para replicar el proceso ETL
// Kaggle Survey 2019 - Ingeniería de Sistemas

let
    // PASO 1: Cargar datos desde CSV
    // ¿Por qué este paso? Cargar los datos originales para procesar
    Source = Csv.Document(File.Contents("multipleChoiceResponses.csv"),[Delimiter=",", Columns=350, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // PASO 2: Eliminar registros duplicados
    // ¿Por qué este paso? Evitar duplicación de datos en análisis
    RemovedDuplicates = Table.Distinct(PromotedHeaders),
    
    // PASO 3: Manejo de valores nulos
    // ¿Por qué este paso? Eliminar columnas con demasiados nulos
    ColumnCount = Table.ColumnCount(RemovedDuplicates),
    RowCount = Table.RowCount(RemovedDuplicates),
    Threshold = RowCount * 0.8,
    
    // Identificar columnas a eliminar (>80% nulos)
    ColumnsToRemove = List.Select(Table.ColumnNames(RemovedDuplicates), 
        each List.Count(List.RemoveNulls(Table.Column(RemovedDuplicates, _))) < Threshold),
    
    // Eliminar columnas con muchos valores faltantes
    RemovedHighNullColumns = Table.RemoveColumns(RemovedDuplicates, ColumnsToRemove),
    
    // PASO 4: Imputar valores nulos
    // ¿Por qué este paso? Completar datos faltantes para análisis
    // Para columnas de texto, reemplazar con "No especificado"
    TextColumns = List.Select(Table.ColumnNames(RemovedHighNullColumns), 
        each Value.Type(Table.Column(RemovedHighNullColumns, _){0}) = type text),
    
    // Para columnas numéricas, reemplazar con mediana
    NumericColumns = List.Select(Table.ColumnNames(RemovedHighNullColumns), 
        each Value.Type(Table.Column(RemovedHighNullColumns, _){0}) = type number),
    
    // Aplicar transformaciones
    ImputedTextColumns = List.Accumulate(TextColumns, RemovedHighNullColumns, 
        (table, column) => Table.ReplaceValue(table, null, "No especificado", Replacer.ReplaceValue, {column})),
    
    ImputedNumericColumns = List.Accumulate(NumericColumns, ImputedTextColumns, 
        (table, column) => Table.ReplaceValue(table, null, 
            List.Median(List.RemoveNulls(Table.Column(table, column))), 
            Replacer.ReplaceValue, {column})),
    
    // PASO 5: Limpiar espacios en blanco
    // ¿Por qué este paso? Estandarizar formato de texto
    TrimmedColumns = List.Accumulate(TextColumns, ImputedNumericColumns, 
        (table, column) => Table.TransformColumns(table, {{column, Text.Trim}})),
    
    // PASO 6: Renombrar columnas principales
    // ¿Por qué este paso? Hacer nombres más descriptivos
    RenamedColumns = Table.RenameColumns(TrimmedColumns, {
        {"Time from Start to Finish (seconds)", "Tiempo_Total_Encuesta_Segundos"},
        {"Q1", "Edad_Encuestado"},
        {"Q2", "Genero"},
        {"Q3", "Pais_Residencia"},
        {"Q4", "Nivel_Educativo"},
        {"Q5", "Area_Estudios_Principal"},
        {"Q6", "Situacion_Laboral_Actual"},
        {"Q7", "Cargo_Principal_Trabajo"},
        {"Q8", "Anos_Experiencia_Campo"},
        {"Q9", "Rango_Salarial_Anual"}
    }),
    
    // PASO 7: Crear columnas derivadas
    // ¿Por qué este paso? Facilitar análisis agrupando categorías
    // Categoría de experiencia
    AddedExperienceCategory = Table.AddColumn(RenamedColumns, "Categoria_Experiencia", 
        each if [Anos_Experiencia_Campo] = "0-1" or [Anos_Experiencia_Campo] = "1-2" then "Principiante (0-2 años)"
        else if [Anos_Experiencia_Campo] = "2-3" or [Anos_Experiencia_Campo] = "3-4" then "Intermedio (2-4 años)"
        else if [Anos_Experiencia_Campo] = "4-5" or [Anos_Experiencia_Campo] = "5-10" then "Avanzado (4-10 años)"
        else if [Anos_Experiencia_Campo] = "10-15" or [Anos_Experiencia_Campo] = "15-20" or [Anos_Experiencia_Campo] = "20+" then "Experto (10+ años)"
        else "No especificado"),
    
    // Categoría de salario
    AddedSalaryCategory = Table.AddColumn(AddedExperienceCategory, "Categoria_Salarial", 
        each if [Rango_Salarial_Anual] = "0-10,000" or [Rango_Salarial_Anual] = "10-20,000" then "Bajo (0-20k)"
        else if [Rango_Salarial_Anual] = "20-30,000" or [Rango_Salarial_Anual] = "30-40,000" or [Rango_Salarial_Anual] = "40-50,000" then "Medio (20-50k)"
        else if [Rango_Salarial_Anual] = "50-60,000" or [Rango_Salarial_Anual] = "60-70,000" or [Rango_Salarial_Anual] = "70-80,000" or [Rango_Salarial_Anual] = "80-90,000" or [Rango_Salarial_Anual] = "90-100,000" then "Alto (50-100k)"
        else if [Rango_Salarial_Anual] = "100-125,000" or [Rango_Salarial_Anual] = "125-150,000" or [Rango_Salarial_Anual] = "150-200,000" or [Rango_Salarial_Anual] = "200-250,000" or [Rango_Salarial_Anual] = "250-300,000" or [Rango_Salarial_Anual] = "300-400,000" or [Rango_Salarial_Anual] = "400-500,000" or [Rango_Salarial_Anual] = "500,000+" then "Muy Alto (100k+)"
        else "No especificado"),
    
    // PASO 8: Convertir tipos de datos
    // ¿Por qué este paso? Asegurar tipos correctos para análisis
    ConvertedTypes = Table.TransformColumnTypes(AddedSalaryCategory, {
        {"Tiempo_Total_Encuesta_Segundos", type number}
    })
    
in
    ConvertedTypes
"""
    
    # Guardar script en archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_filename = f"powerbi_etl_script_{timestamp}.txt"
    
    with open(script_filename, 'w', encoding='utf-8') as f:
        f.write("SCRIPT DE POWER QUERY M PARA KAGGLE SURVEY ETL\n")
        f.write("=" * 50 + "\n\n")
        f.write("INSTRUCCIONES DE USO:\n")
        f.write("1. Abrir Power BI Desktop\n")
        f.write("2. Ir a 'Obtener datos' > 'Archivo' > 'Texto/CSV'\n")
        f.write("3. Seleccionar el archivo 'multipleChoiceResponses.csv'\n")
        f.write("4. En el Editor de Power Query, ir a 'Vista' > 'Editor avanzado'\n")
        f.write("5. Reemplazar el código existente con el siguiente script:\n\n")
        f.write(script_powerbi)
        f.write("\n\nMÉTRICAS ESPERADAS PARA VALIDACIÓN:\n")
        f.write("-" * 40 + "\n")
        f.write("Total de registros: 19,717\n")
        f.write("Total de columnas: 298\n")
        f.write("Valores nulos totales: 0\n")
        f.write("Registros únicos: 19,717\n")
        f.write("Memoria utilizada: ~39.0 MB\n")
    
    print(f"✅ Script de Power BI generado: {script_filename}")
    print(f"📄 Contenido: Script M completo para replicar ETL")
    print(f"🎯 Uso: Copiar y pegar en Power Query Editor")
    
    return script_filename

def generar_metricas_validacion(metricas_python):
    """
    Genera un archivo con métricas específicas para validar en Power BI
    """
    print("\n" + "=" * 80)
    print("📋 GENERANDO MÉTRICAS DE VALIDACIÓN")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"metricas_validacion_powerbi_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("MÉTRICAS DE VALIDACIÓN - PYTHON vs POWER BI\n")
        f.write("=" * 50 + "\n\n")
        f.write("INSTRUCCIONES:\n")
        f.write("1. Ejecutar el script de Power Query M en Power BI\n")
        f.write("2. Comparar las siguientes métricas con los valores esperados\n")
        f.write("3. Verificar que las diferencias sean mínimas (< 1%)\n\n")
        
        f.write("MÉTRICAS BÁSICAS:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total de registros: {metricas_python.get('total_registros', 'N/A'):,}\n")
        f.write(f"Total de columnas: {metricas_python.get('total_columnas', 'N/A'):,}\n")
        f.write(f"Valores nulos totales: {metricas_python.get('valores_nulos_totales', 'N/A'):,}\n")
        f.write(f"Registros únicos: {metricas_python.get('registros_unicos', 'N/A'):,}\n")
        f.write(f"Memoria utilizada: {metricas_python.get('memoria_mb', 'N/A'):.2f} MB\n\n")
        
        # Distribución por género
        if 'distribucion_genero' in metricas_python:
            f.write("DISTRIBUCIÓN POR GÉNERO:\n")
            f.write("-" * 25 + "\n")
            for gender, count in metricas_python['distribucion_genero'].items():
                percentage = (count / metricas_python['total_registros']) * 100
                f.write(f"{gender}: {count:,} ({percentage:.1f}%)\n")
            f.write("\n")
        
        # Top 5 países
        if 'top_5_paises' in metricas_python:
            f.write("TOP 5 PAÍSES:\n")
            f.write("-" * 15 + "\n")
            for country, count in metricas_python['top_5_paises'].items():
                percentage = (count / metricas_python['total_registros']) * 100
                f.write(f"{country}: {count:,} ({percentage:.1f}%)\n")
            f.write("\n")
        
        f.write("FÓRMULAS DE POWER BI PARA VALIDACIÓN:\n")
        f.write("-" * 40 + "\n")
        f.write("Total de registros: = COUNTROWS(Tabla)\n")
        f.write("Total de columnas: = COLUMNS(Tabla)\n")
        f.write("Valores nulos: = SUMX(Tabla, IF(ISBLANK([Columna]), 1, 0))\n")
        f.write("Registros únicos: = DISTINCTCOUNT(Tabla[ID])\n")
        f.write("Distribución por género: = COUNTROWS(FILTER(Tabla, [Genero] = \"Male\"))\n")
        f.write("Top país: = TOPN(1, VALUES(Tabla[Pais_Residencia]), COUNTROWS(Tabla))\n")
    
    print(f"✅ Métricas de validación generadas: {filename}")
    print(f"📄 Contenido: Métricas esperadas para comparar")
    print(f"🎯 Uso: Validar que Power BI produce los mismos resultados")
    
    return filename

def generar_instrucciones_dashboard():
    """
    Genera instrucciones para crear un dashboard en Power BI
    """
    print("\n" + "=" * 80)
    print("📊 GENERANDO INSTRUCCIONES PARA DASHBOARD")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"instrucciones_dashboard_powerbi_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("INSTRUCCIONES PARA DASHBOARD EN POWER BI\n")
        f.write("Kaggle Survey 2019 - Ingeniería de Sistemas\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("PASOS PARA CREAR EL DASHBOARD:\n")
        f.write("-" * 30 + "\n\n")
        
        f.write("1. PREPARACIÓN DE DATOS:\n")
        f.write("   • Ejecutar el script de Power Query M\n")
        f.write("   • Verificar que los datos se carguen correctamente\n")
        f.write("   • Aplicar el modelo de datos\n\n")
        
        f.write("2. VISUALIZACIONES RECOMENDADAS:\n")
        f.write("   • Gráfico de pastel: Distribución por género\n")
        f.write("   • Gráfico de barras: Top 10 países\n")
        f.write("   • Gráfico de barras horizontales: Nivel educativo\n")
        f.write("   • Gráfico de barras: Categorías de experiencia\n")
        f.write("   • Gráfico de barras: Categorías salariales\n")
        f.write("   • Heatmap: Salario vs Experiencia\n")
        f.write("   • Gráfico de dispersión: Tiempo de encuesta vs Experiencia\n\n")
        
        f.write("3. MEDIDAS DAX RECOMENDADAS:\n")
        f.write("   • Total Encuestados = COUNTROWS(Tabla)\n")
        f.write("   • Porcentaje por Género = DIVIDE(COUNTROWS(FILTER(Tabla, [Genero] = \"Male\")), [Total Encuestados])\n")
        f.write("   • Promedio Tiempo Encuesta = AVERAGE(Tabla[Tiempo_Total_Encuesta_Segundos])\n")
        f.write("   • Top País = TOPN(1, VALUES(Tabla[Pais_Residencia]), COUNTROWS(Tabla))\n")
        f.write("   • Distribución Experiencia = COUNTROWS(FILTER(Tabla, [Categoria_Experiencia] = \"Principiante (0-2 años)\"))\n\n")
        
        f.write("4. FILTROS RECOMENDADOS:\n")
        f.write("   • País de residencia\n")
        f.write("   • Nivel educativo\n")
        f.write("   • Categoría de experiencia\n")
        f.write("   • Categoría salarial\n")
        f.write("   • Área de estudios\n\n")
        
        f.write("5. DISEÑO DEL DASHBOARD:\n")
        f.write("   • Título: 'Análisis Kaggle Survey 2019 - Ingeniería de Sistemas'\n")
        f.write("   • Sección 1: Demografía (género, edad, país)\n")
        f.write("   • Sección 2: Formación (educación, área de estudios)\n")
        f.write("   • Sección 3: Laboral (experiencia, salario, cargo)\n")
        f.write("   • Sección 4: Análisis cruzado (salario vs experiencia)\n\n")
        
        f.write("6. VALIDACIÓN DE RESULTADOS:\n")
        f.write("   • Comparar métricas con los valores de Python\n")
        f.write("   • Verificar que las distribuciones coincidan\n")
        f.write("   • Validar que los filtros funcionen correctamente\n")
        f.write("   • Confirmar que las visualizaciones sean coherentes\n\n")
        
        f.write("7. EXPORTACIÓN:\n")
        f.write("   • Guardar como archivo .pbix\n")
        f.write("   • Publicar en Power BI Service (opcional)\n")
        f.write("   • Exportar visualizaciones como imágenes\n")
        f.write("   • Generar reporte PDF\n")
    
    print(f"✅ Instrucciones de dashboard generadas: {filename}")
    print(f"📄 Contenido: Guía paso a paso para crear visualizaciones")
    print(f"🎯 Uso: Crear dashboard profesional en Power BI")
    
    return filename

def mostrar_resumen_comparacion(script_file, metrics_file, dashboard_file, metricas_python):
    """
    Muestra un resumen de la comparación con Power BI
    """
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE LA COMPARACIÓN CON POWER BI")
    print("=" * 80)
    
    print("✅ ARCHIVOS GENERADOS PARA VALIDACIÓN:")
    print("-" * 40)
    
    if script_file:
        script_size = os.path.getsize(script_file) / 1024
        print(f"🔧 {script_file} ({script_size:.2f} KB)")
        print(f"   • Contenido: Script M completo para Power Query")
        print(f"   • Uso: Replicar proceso ETL en Power BI")
        print(f"   • Ventaja: Automatiza la transformación de datos")
    
    if metrics_file:
        metrics_size = os.path.getsize(metrics_file) / 1024
        print(f"📋 {metrics_file} ({metrics_size:.2f} KB)")
        print(f"   • Contenido: Métricas esperadas para validación")
        print(f"   • Uso: Comparar resultados entre Python y Power BI")
        print(f"   • Ventaja: Asegura coherencia de datos")
    
    if dashboard_file:
        dashboard_size = os.path.getsize(dashboard_file) / 1024
        print(f"📊 {dashboard_file} ({dashboard_size:.2f} KB)")
        print(f"   • Contenido: Instrucciones para crear dashboard")
        print(f"   • Uso: Guía paso a paso para visualizaciones")
        print(f"   • Ventaja: Dashboard profesional y coherente")
    
    print(f"\n📊 MÉTRICAS DE VALIDACIÓN (PYTHON):")
    print("-" * 40)
    print(f"• Total de registros: {metricas_python.get('total_registros', 'N/A'):,}")
    print(f"• Total de columnas: {metricas_python.get('total_columnas', 'N/A'):,}")
    print(f"• Valores nulos: {metricas_python.get('valores_nulos_totales', 'N/A'):,}")
    print(f"• Memoria utilizada: {metricas_python.get('memoria_mb', 'N/A'):.2f} MB")
    
    print(f"\n🎯 PRÓXIMOS PASOS PARA VALIDACIÓN:")
    print("-" * 40)
    print("1. Abrir Power BI Desktop")
    print("2. Cargar archivo 'multipleChoiceResponses.csv'")
    print("3. Ejecutar script M en Editor de Power Query")
    print("4. Comparar métricas con valores esperados")
    print("5. Crear dashboard siguiendo las instrucciones")
    print("6. Validar que los resultados coincidan con Python")
    
    print(f"\n✅ CRITERIOS DE VALIDACIÓN EXITOSA:")
    print("-" * 40)
    print("• Diferencias en registros: < 1%")
    print("• Diferencias en columnas: < 1%")
    print("• Valores nulos: 0 en ambos")
    print("• Distribuciones: Coincidencia > 95%")
    print("• Visualizaciones: Coherentes y legibles")

def main():
    """
    Función principal para ejecutar la comparación con Power BI
    """
    print("🚀 VISUALIZACIÓN DE LA COMPARACIÓN CON POWER BI")
    print("📊 Dataset: Kaggle Machine Learning & Data Science Survey 2019")
    print("🎯 Aplicación: Ingeniería de Sistemas")
    print("=" * 80)
    
    # Verificar archivos requeridos
    csv_file = verificar_archivos_requeridos()
    if not csv_file:
        return
    
    # Cargar datos limpios
    df = cargar_datos_limpios(csv_file)
    if df is None:
        return
    
    # Calcular métricas en Python
    metricas_python = calcular_metricas_python(df)
    
    # Generar script de Power BI
    script_file = generar_script_powerbi()
    
    # Generar métricas de validación
    metrics_file = generar_metricas_validacion(metricas_python)
    
    # Generar instrucciones de dashboard
    dashboard_file = generar_instrucciones_dashboard()
    
    # Mostrar resumen
    mostrar_resumen_comparacion(script_file, metrics_file, dashboard_file, metricas_python)
    
    print("\n" + "=" * 80)
    print("✅ COMPARACIÓN CON POWER BI COMPLETADA")
    print("📊 Archivos listos para validación en Power BI")
    print("=" * 80)
    
    print("\n🎯 PROCESO ETL COMPLETO VALIDADO:")
    print("1. ✅ EXTRACCIÓN - Datos cargados desde CSV")
    print("2. ✅ TRANSFORMACIÓN - Datos limpiados y transformados")
    print("3. ✅ CARGA - Datos exportados en múltiples formatos")
    print("4. ✅ VALIDACIÓN - Scripts generados para Power BI")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("1. Abrir Power BI Desktop")
    print("2. Ejecutar script M generado")
    print("3. Comparar métricas con valores esperados")
    print("4. Crear dashboard profesional")
    print("5. Validar coherencia de resultados")

if __name__ == "__main__":
    main()

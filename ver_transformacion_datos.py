#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Visualizar la Fase de TRANSFORMACIÓN del Proceso ETL
Kaggle Survey 2019 - Ingeniería de Sistemas

Este script muestra únicamente la fase de transformación con visualizaciones
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def verificar_archivo():
    """
    Verifica que el archivo CSV existe
    """
    archivo = "multipleChoiceResponses.csv"
    if not os.path.exists(archivo):
        print(f"❌ ERROR: No se encontró el archivo {archivo}")
        print("Asegúrate de que el archivo esté en el directorio actual")
        return False
    return True

def cargar_datos_originales():
    """
    Carga los datos originales para la transformación
    """
    print("=" * 80)
    print("🚀 FASE 2: TRANSFORMACIÓN DE DATOS")
    print("=" * 80)
    
    archivo = "multipleChoiceResponses.csv"
    
    try:
        print(f"📁 Cargando dataset original desde: {archivo}")
        df = pd.read_csv(archivo, encoding='utf-8')
        
        print(f"✅ Dataset original cargado")
        print(f"📊 Dimensiones originales: {df.shape}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al cargar el dataset: {str(e)}")
        return None

def mostrar_analisis_exploratorio(df):
    """
    FASE 2A: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    """
    print("\n" + "=" * 80)
    print("📊 FASE 2A: ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
    print("=" * 80)
    
    # 1. Información general del dataset
    print("📊 1. INFORMACIÓN GENERAL DEL DATASET")
    print("-" * 50)
    print(f"Dimensiones: {df.shape}")
    print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 2. Tipos de datos
    print("\n📋 2. TIPOS DE DATOS")
    print("-" * 50)
    tipos = df.dtypes.value_counts()
    for tipo, cantidad in tipos.items():
        print(f"   • {tipo}: {cantidad:,} columnas")
    
    # 3. Valores faltantes
    print("\n❌ 3. ANÁLISIS DE VALORES FALTANTES")
    print("-" * 50)
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    
    print(f"Total de columnas con valores faltantes: {(missing_data > 0).sum()}")
    print(f"Total de valores faltantes: {missing_data.sum():,}")
    print(f"Porcentaje promedio de valores faltantes: {missing_percentage.mean():.2f}%")
    
    # Mostrar las 10 columnas con más valores faltantes
    missing_summary = pd.DataFrame({
        'Valores_Faltantes': missing_data,
        'Porcentaje': missing_percentage
    }).sort_values('Valores_Faltantes', ascending=False)
    
    print("\n🔝 Top 10 columnas con más valores faltantes:")
    for i, (col, row) in enumerate(missing_summary.head(10).iterrows(), 1):
        print(f"   {i:2d}. {col}: {row['Valores_Faltantes']:,} ({row['Porcentaje']:.1f}%)")
    
    # 4. Valores únicos por columna
    print("\n🔢 4. ANÁLISIS DE VALORES ÚNICOS")
    print("-" * 50)
    unique_counts = df.nunique()
    print(f"Columna con más valores únicos: {unique_counts.idxmax()} ({unique_counts.max()} valores)")
    print(f"Columna con menos valores únicos: {unique_counts.idxmin()} ({unique_counts.min()} valores)")
    
    # 5. Registros duplicados
    print("\n🔄 5. ANÁLISIS DE REGISTROS DUPLICADOS")
    print("-" * 50)
    duplicates = df.duplicated().sum()
    print(f"Registros duplicados: {duplicates}")
    print(f"Porcentaje de duplicados: {(duplicates / len(df)) * 100:.2f}%")
    
    # 6. Estadísticas descriptivas para columnas numéricas
    print("\n📈 6. ESTADÍSTICAS DESCRIPTIVAS (COLUMNAS NUMÉRICAS)")
    print("-" * 50)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"Columnas numéricas encontradas: {len(numeric_cols)}")
        print("\nEstadísticas de la columna 'Time from Start to Finish (seconds)':")
        if 'Time from Start to Finish (seconds)' in df.columns:
            tiempo_col = pd.to_numeric(df['Time from Start to Finish (seconds)'], errors='coerce')
            print(f"   • Media: {tiempo_col.mean():.2f} segundos")
            print(f"   • Mediana: {tiempo_col.median():.2f} segundos")
            print(f"   • Desviación estándar: {tiempo_col.std():.2f} segundos")
            print(f"   • Mínimo: {tiempo_col.min():.2f} segundos")
            print(f"   • Máximo: {tiempo_col.max():.2f} segundos")
    else:
        print("No se encontraron columnas numéricas")
    
    # 7. Análisis de columnas categóricas principales
    print("\n📊 7. ANÁLISIS DE COLUMNAS CATEGÓRICAS PRINCIPALES")
    print("-" * 50)
    
    key_columns = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9']
    for col in key_columns:
        if col in df.columns:
            print(f"\n{col}:")
            value_counts = df[col].value_counts().head(5)
            for value, count in value_counts.items():
                percentage = (count / len(df)) * 100
                print(f"  • {value}: {count:,} ({percentage:.1f}%)")

def mostrar_limpieza_datos(df):
    """
    FASE 2B: LIMPIEZA Y TRANSFORMACIÓN DE DATOS
    """
    print("\n" + "=" * 80)
    print("🧹 FASE 2B: LIMPIEZA Y TRANSFORMACIÓN DE DATOS")
    print("=" * 80)
    
    df_clean = df.copy()
    print(f"📊 Dataset inicial: {df_clean.shape}")
    
    # 1. Eliminación de registros duplicados
    print("\n🔄 1. ELIMINACIÓN DE REGISTROS DUPLICADOS")
    print("-" * 50)
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed_duplicates = initial_rows - len(df_clean)
    print(f"Registros eliminados por duplicación: {removed_duplicates}")
    print(f"Registros restantes: {len(df_clean):,}")
    
    # 2. Manejo de valores nulos
    print("\n❌ 2. MANEJO DE VALORES NULOS")
    print("-" * 50)
    
    # Estrategia: Para columnas con más del 80% de valores faltantes, las eliminamos
    missing_percentage = (df_clean.isnull().sum() / len(df_clean)) * 100
    
    # Identificar columnas a eliminar
    columns_to_drop = missing_percentage[missing_percentage > 80].index
    print(f"Columnas identificadas para eliminar (>80% valores faltantes): {len(columns_to_drop)}")
    
    # Mostrar algunas columnas que se van a eliminar
    if len(columns_to_drop) > 0:
        print("\n🔝 Ejemplos de columnas a eliminar:")
        for i, col in enumerate(columns_to_drop[:5], 1):
            porcentaje = missing_percentage[col]
            print(f"   {i}. {col}: {porcentaje:.1f}% valores faltantes")
    
    # Eliminar columnas con muchos valores faltantes
    df_clean = df_clean.drop(columns=columns_to_drop)
    print(f"Columnas eliminadas: {len(columns_to_drop)}")
    print(f"Columnas restantes: {df_clean.shape[1]}")
    
    # Para columnas categóricas, imputar con "No especificado"
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    print(f"\nImputando valores nulos en {len(categorical_cols)} columnas categóricas...")
    
    for col in categorical_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna('No especificado')
    
    # Para columnas numéricas, imputar con la mediana
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    print(f"Imputando valores nulos en {len(numeric_cols)} columnas numéricas...")
    
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    print(f"Valores nulos restantes: {df_clean.isnull().sum().sum()}")
    
    # 3. Limpieza de espacios en blanco
    print("\n🧹 3. LIMPIEZA DE ESPACIOS EN BLANCO")
    print("-" * 50)
    
    # Eliminar espacios al inicio y final de strings
    for col in categorical_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()
    
    print("Espacios en blanco eliminados de todas las columnas de texto")
    
    # 4. Normalización de datos
    print("\n🔄 4. NORMALIZACIÓN DE DATOS")
    print("-" * 50)
    
    # Normalizar texto a minúsculas para ciertas columnas
    text_columns = ['Q1_OTHER_TEXT', 'Q6_OTHER_TEXT', 'Q7_OTHER_TEXT', 'Q11_OTHER_TEXT']
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.lower()
            print(f"Columna {col} normalizada a minúsculas")
    
    # 5. Conversión de tipos de datos
    print("\n🔄 5. CONVERSIÓN DE TIPOS DE DATOS")
    print("-" * 50)
    
    # Convertir columna de tiempo a numérico
    if 'Time from Start to Finish (seconds)' in df_clean.columns:
        df_clean['Time from Start to Finish (seconds)'] = pd.to_numeric(
            df_clean['Time from Start to Finish (seconds)'], errors='coerce'
        )
        print("Columna 'Time from Start to Finish (seconds)' convertida a numérico")
    
    return df_clean

def mostrar_renombrado_columnas(df_clean):
    """
    FASE 2C: RENOMBRADO DE COLUMNAS
    """
    print("\n" + "=" * 80)
    print("📝 FASE 2C: RENOMBRADO DE COLUMNAS")
    print("=" * 80)
    
    # Crear mapeo de columnas
    column_mapping = {
        # Información general
        'Time from Start to Finish (seconds)': 'Tiempo_Total_Encuesta_Segundos',
        
        # Demografía y formación
        'Q1': 'Edad_Encuestado',
        'Q1_OTHER_TEXT': 'Edad_Encuestado_Texto_Libre',
        'Q2': 'Genero',
        'Q3': 'Pais_Residencia',
        'Q4': 'Nivel_Educativo',
        'Q5': 'Area_Estudios_Principal',
        
        # Situación laboral
        'Q6': 'Situacion_Laboral_Actual',
        'Q6_OTHER_TEXT': 'Situacion_Laboral_Texto_Libre',
        'Q7': 'Cargo_Principal_Trabajo',
        'Q7_OTHER_TEXT': 'Cargo_Principal_Texto_Libre',
        'Q8': 'Anos_Experiencia_Campo',
        'Q9': 'Rango_Salarial_Anual',
        
        # Lenguajes y herramientas
        'Q10': 'Lenguajes_Programacion_Habituales',
        'Q11_Part_1': 'IDE_Jupyter_IPython',
        'Q11_Part_2': 'IDE_RStudio',
        'Q11_Part_3': 'IDE_PyCharm',
        'Q11_Part_4': 'IDE_Visual_Studio_Code',
        'Q11_Part_5': 'IDE_nteract',
        'Q11_Part_6': 'IDE_Atom',
        'Q11_Part_7': 'IDE_MATLAB',
        'Q11_OTHER_TEXT': 'IDE_Otros_Texto_Libre',
        
        # Plataformas y hardware
        'Q12_MULTIPLE_CHOICE': 'Herramienta_Analisis_Datos_Principal',
        'Q12_Part_1_TEXT': 'Herramienta_Estadistica_Basica_Texto',
        'Q12_Part_2_TEXT': 'Herramienta_Estadistica_Avanzada_Texto',
        'Q12_Part_3_TEXT': 'Herramienta_BI_Texto',
        'Q12_Part_4_TEXT': 'Herramienta_Desarrollo_Local_Texto',
        'Q12_Part_5_TEXT': 'Herramienta_Cloud_APIs_Texto',
        'Q12_OTHER_TEXT': 'Herramienta_Analisis_Otros_Texto',
    }
    
    # Crear mapeo solo para columnas que existen en el dataset
    existing_mapping = {k: v for k, v in column_mapping.items() if k in df_clean.columns}
    
    print(f"📝 RENOMBRANDO {len(existing_mapping)} COLUMNAS")
    print("-" * 50)
    
    # Mostrar ejemplos de renombrado
    print("🔹 EJEMPLOS DE RENOMBRADO:")
    for i, (old_name, new_name) in enumerate(list(existing_mapping.items())[:10], 1):
        print(f"   {i:2d}. {old_name}")
        print(f"       → {new_name}")
    
    if len(existing_mapping) > 10:
        print(f"   ... y {len(existing_mapping) - 10} columnas más")
    
    # Aplicar renombrado
    df_renamed = df_clean.rename(columns=existing_mapping)
    
    print(f"\n✅ RENOMBRADO COMPLETADO")
    print(f"📊 Columnas renombradas: {len(existing_mapping)}")
    
    return df_renamed

def mostrar_columnas_derivadas(df_renamed):
    """
    FASE 2D: CREACIÓN DE COLUMNAS DERIVADAS
    """
    print("\n" + "=" * 80)
    print("➕ FASE 2D: CREACIÓN DE COLUMNAS DERIVADAS")
    print("=" * 80)
    
    df_final = df_renamed.copy()
    
    # 1. Crear categoría de experiencia
    print("🔹 1. CREANDO CATEGORÍA DE EXPERIENCIA")
    print("-" * 40)
    
    if 'Anos_Experiencia_Campo' in df_final.columns:
        def categorize_experience(exp):
            if pd.isna(exp) or exp == 'No especificado':
                return 'No especificado'
            elif exp in ['0-1', '1-2']:
                return 'Principiante (0-2 años)'
            elif exp in ['2-3', '3-4']:
                return 'Intermedio (2-4 años)'
            elif exp in ['4-5', '5-10']:
                return 'Avanzado (4-10 años)'
            else:
                return 'Experto (10+ años)'
        
        df_final['Categoria_Experiencia'] = df_final['Anos_Experiencia_Campo'].apply(categorize_experience)
        
        # Mostrar distribución
        exp_dist = df_final['Categoria_Experiencia'].value_counts()
        print("Distribución de categorías de experiencia:")
        for categoria, count in exp_dist.items():
            percentage = (count / len(df_final)) * 100
            print(f"   • {categoria}: {count:,} ({percentage:.1f}%)")
    
    # 2. Crear categoría de salario
    print("\n🔹 2. CREANDO CATEGORÍA DE SALARIO")
    print("-" * 40)
    
    if 'Rango_Salarial_Anual' in df_final.columns:
        def categorize_salary(salary):
            if pd.isna(salary) or salary in ['No especificado', 'I do not wish to disclose my approximate yearly compensation']:
                return 'No especificado'
            elif salary in ['0-10,000', '10-20,000']:
                return 'Bajo (0-20k)'
            elif salary in ['20-30,000', '30-40,000', '40-50,000']:
                return 'Medio (20-50k)'
            elif salary in ['50-60,000', '60-70,000', '70-80,000', '80-90,000', '90-100,000']:
                return 'Alto (50-100k)'
            else:
                return 'Muy Alto (100k+)'
        
        df_final['Categoria_Salarial'] = df_final['Rango_Salarial_Anual'].apply(categorize_salary)
        
        # Mostrar distribución
        sal_dist = df_final['Categoria_Salarial'].value_counts()
        print("Distribución de categorías salariales:")
        for categoria, count in sal_dist.items():
            percentage = (count / len(df_final)) * 100
            print(f"   • {categoria}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n✅ COLUMNAS DERIVADAS CREADAS")
    print(f"📊 Total de columnas finales: {df_final.shape[1]}")
    
    return df_final

def mostrar_comparacion_antes_despues(df_original, df_final):
    """
    Muestra la comparación antes y después de la transformación
    """
    print("\n" + "=" * 80)
    print("📊 COMPARACIÓN ANTES Y DESPUÉS DE LA TRANSFORMACIÓN")
    print("=" * 80)
    
    print("📈 MÉTRICAS DE TRANSFORMACIÓN:")
    print("-" * 40)
    print(f"Registros originales: {df_original.shape[0]:,}")
    print(f"Registros finales: {df_final.shape[0]:,}")
    print(f"Reducción de registros: {df_original.shape[0] - df_final.shape[0]:,}")
    
    print(f"\nColumnas originales: {df_original.shape[1]:,}")
    print(f"Columnas finales: {df_final.shape[1]:,}")
    print(f"Reducción de columnas: {df_original.shape[1] - df_final.shape[1]:,}")
    
    print(f"\nValores nulos originales: {df_original.isnull().sum().sum():,}")
    print(f"Valores nulos finales: {df_final.isnull().sum().sum():,}")
    print(f"Valores nulos eliminados: {df_original.isnull().sum().sum() - df_final.isnull().sum().sum():,}")
    
    print(f"\nMemoria original: {df_original.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Memoria final: {df_final.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Reducción de memoria: {((df_original.memory_usage(deep=True).sum() - df_final.memory_usage(deep=True).sum()) / df_original.memory_usage(deep=True).sum()) * 100:.1f}%")
    
    # Mostrar primeras filas del dataset transformado
    print("\n📋 PRIMERAS 5 FILAS DEL DATASET TRANSFORMADO:")
    print("-" * 50)
    
    # Seleccionar columnas principales para mostrar
    columnas_principales = [
        'Tiempo_Total_Encuesta_Segundos', 'Edad_Encuestado', 'Genero', 
        'Pais_Residencia', 'Nivel_Educativo', 'Categoria_Experiencia', 'Categoria_Salarial'
    ]
    
    columnas_existentes = [col for col in columnas_principales if col in df_final.columns]
    
    if columnas_existentes:
        df_muestra = df_final[columnas_existentes].head(5)
        print(df_muestra.to_string(index=True))
    else:
        print("No se encontraron las columnas principales transformadas")

def main():
    """
    Función principal para ejecutar la visualización de transformación
    """
    print("🚀 VISUALIZACIÓN DE LA FASE DE TRANSFORMACIÓN")
    print("📊 Dataset: Kaggle Machine Learning & Data Science Survey 2019")
    print("🎯 Aplicación: Ingeniería de Sistemas")
    print("=" * 80)
    
    # Verificar archivo
    if not verificar_archivo():
        return
    
    # Cargar datos originales
    df_original = cargar_datos_originales()
    if df_original is None:
        return
    
    # Mostrar análisis exploratorio
    mostrar_analisis_exploratorio(df_original)
    
    # Mostrar limpieza de datos
    df_clean = mostrar_limpieza_datos(df_original)
    
    # Mostrar renombrado de columnas
    df_renamed = mostrar_renombrado_columnas(df_clean)
    
    # Mostrar columnas derivadas
    df_final = mostrar_columnas_derivadas(df_renamed)
    
    # Mostrar comparación antes y después
    mostrar_comparacion_antes_despues(df_original, df_final)
    
    print("\n" + "=" * 80)
    print("✅ FASE DE TRANSFORMACIÓN COMPLETADA")
    print("📊 Dataset transformado listo para la siguiente fase: CARGA")
    print("=" * 80)
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Ejecutar: python ver_carga_datos.py")
    print("2. O ejecutar todo: python ejecutar_proceso_completo.py")
    
    return df_final

if __name__ == "__main__":
    main()

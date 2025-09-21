#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Visualizar la Fase de EXTRACCIÓN del Proceso ETL
Kaggle Survey 2019 - Ingeniería de Sistemas

Este script muestra únicamente la fase de extracción con visualizaciones
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

def extraer_datos():
    """
    FASE 1: EXTRACCIÓN DE DATOS
    """
    print("=" * 80)
    print("🚀 FASE 1: EXTRACCIÓN DE DATOS")
    print("=" * 80)
    
    archivo = "multipleChoiceResponses.csv"
    
    try:
        print(f"📁 Cargando dataset desde: {archivo}")
        print("⏳ Esto puede tomar unos segundos...")
        
        # Cargar el dataset
        df = pd.read_csv(archivo, encoding='utf-8')
        
        print(f"✅ Dataset cargado exitosamente")
        print(f"📊 Dimensiones del dataset: {df.shape}")
        print(f"📋 Número de registros: {df.shape[0]:,}")
        print(f"📋 Número de columnas: {df.shape[1]:,}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al cargar el dataset: {str(e)}")
        return None

def mostrar_informacion_general(df):
    """
    Muestra información general del dataset
    """
    print("\n" + "=" * 80)
    print("📊 INFORMACIÓN GENERAL DEL DATASET")
    print("=" * 80)
    
    # Información básica
    print(f"📏 Dimensiones: {df.shape[0]:,} filas × {df.shape[1]:,} columnas")
    print(f"💾 Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"📅 Fecha de carga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Tipos de datos
    print(f"\n📋 TIPOS DE DATOS:")
    tipos = df.dtypes.value_counts()
    for tipo, cantidad in tipos.items():
        print(f"   • {tipo}: {cantidad:,} columnas")
    
    # Valores faltantes
    total_nulos = df.isnull().sum().sum()
    total_celdas = df.shape[0] * df.shape[1]
    porcentaje_nulos = (total_nulos / total_celdas) * 100
    
    print(f"\n❌ VALORES FALTANTES:")
    print(f"   • Total de valores nulos: {total_nulos:,}")
    print(f"   • Total de celdas: {total_celdas:,}")
    print(f"   • Porcentaje de nulos: {porcentaje_nulos:.2f}%")

def mostrar_primeros_registros(df, n=10):
    """
    Muestra los primeros N registros del dataset
    """
    print("\n" + "=" * 80)
    print(f"📋 PRIMEROS {n} REGISTROS DEL DATASET")
    print("=" * 80)
    
    # Mostrar solo las primeras columnas para que sea legible
    columnas_principales = [
        'Time from Start to Finish (seconds)',
        'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'
    ]
    
    # Verificar qué columnas existen
    columnas_existentes = [col for col in columnas_principales if col in df.columns]
    
    if columnas_existentes:
        print(f"📊 Mostrando columnas principales: {len(columnas_existentes)} de {df.shape[1]}")
        print("\n" + "-" * 80)
        
        # Mostrar los primeros registros
        df_muestra = df[columnas_existentes].head(n)
        
        # Configurar pandas para mostrar todas las columnas
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 30)
        
        print(df_muestra.to_string(index=True))
        
        # Restaurar configuración
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
        pd.reset_option('display.max_colwidth')
        
    else:
        print("⚠️ No se encontraron las columnas principales esperadas")
        print("Mostrando las primeras 10 columnas:")
        print(df.iloc[:n, :10].to_string(index=True))

def mostrar_columnas_principales(df):
    """
    Muestra información sobre las columnas principales
    """
    print("\n" + "=" * 80)
    print("📋 INFORMACIÓN DE COLUMNAS PRINCIPALES")
    print("=" * 80)
    
    # Mapeo de columnas principales
    columnas_info = {
        'Time from Start to Finish (seconds)': 'Tiempo total en segundos que tardó en completar la encuesta',
        'Q1': 'Edad del encuestado',
        'Q2': 'Género',
        'Q3': 'País de residencia',
        'Q4': 'Nivel educativo alcanzado',
        'Q5': 'Área principal de estudios',
        'Q6': 'Situación laboral actual',
        'Q7': 'Cargo principal en el trabajo',
        'Q8': 'Años de experiencia en el campo',
        'Q9': 'Rango salarial anual aproximado'
    }
    
    print("📊 DESCRIPCIÓN DE COLUMNAS PRINCIPALES:")
    print("-" * 50)
    
    for col, descripcion in columnas_info.items():
        if col in df.columns:
            valores_unicos = df[col].nunique()
            valores_nulos = df[col].isnull().sum()
            print(f"\n🔹 {col}")
            print(f"   📝 Descripción: {descripcion}")
            print(f"   🔢 Valores únicos: {valores_unicos:,}")
            print(f"   ❌ Valores nulos: {valores_nulos:,}")
            
            # Mostrar algunos valores de ejemplo
            valores_ejemplo = df[col].dropna().head(3).tolist()
            if valores_ejemplo:
                print(f"   📋 Ejemplos: {', '.join(map(str, valores_ejemplo))}")
        else:
            print(f"\n⚠️ {col} - NO ENCONTRADA")

def mostrar_estadisticas_basicas(df):
    """
    Muestra estadísticas básicas del dataset
    """
    print("\n" + "=" * 80)
    print("📈 ESTADÍSTICAS BÁSICAS")
    print("=" * 80)
    
    # Estadísticas para columnas numéricas
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    if len(columnas_numericas) > 0:
        print(f"📊 COLUMNAS NUMÉRICAS ({len(columnas_numericas)} columnas):")
        print("-" * 40)
        
        for col in columnas_numericas[:5]:  # Mostrar solo las primeras 5
            valores = df[col].dropna()
            if len(valores) > 0:
                print(f"\n🔹 {col}:")
                print(f"   • Media: {valores.mean():.2f}")
                print(f"   • Mediana: {valores.median():.2f}")
                print(f"   • Mínimo: {valores.min():.2f}")
                print(f"   • Máximo: {valores.max():.2f}")
                print(f"   • Desviación estándar: {valores.std():.2f}")
    
    # Estadísticas para columnas categóricas principales
    columnas_categoricas = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    columnas_existentes = [col for col in columnas_categoricas if col in df.columns]
    
    if columnas_existentes:
        print(f"\n📊 COLUMNAS CATEGÓRICAS PRINCIPALES:")
        print("-" * 40)
        
        for col in columnas_existentes:
            print(f"\n🔹 {col}:")
            top_valores = df[col].value_counts().head(3)
            for valor, cantidad in top_valores.items():
                porcentaje = (cantidad / len(df)) * 100
                print(f"   • {valor}: {cantidad:,} ({porcentaje:.1f}%)")

def mostrar_relevancia_ingenieria_sistemas():
    """
    Muestra la relevancia del dataset para Ingeniería de Sistemas
    """
    print("\n" + "=" * 80)
    print("🎯 RELEVANCIA PARA INGENIERÍA DE SISTEMAS")
    print("=" * 80)
    
    relevancia = """
    📊 ESTE DATASET ES ALTAMENTE RELEVANTE PARA INGENIERÍA DE SISTEMAS PORQUE:
    
    🏗️ INFRAESTRUCTURA Y ARQUITECTURA:
    • Contiene información sobre herramientas de desarrollo (IDEs, editores)
    • Datos sobre plataformas de computación en la nube (AWS, Azure, GCP)
    • Información sobre bases de datos y sistemas de almacenamiento
    • Herramientas de big data y analytics
    
    💻 DESARROLLO DE SOFTWARE:
    • Lenguajes de programación más utilizados en la industria
    • Frameworks y bibliotecas de machine learning
    • Herramientas de control de versiones y colaboración
    • Metodologías de desarrollo y despliegue
    
    🔧 HERRAMIENTAS Y TECNOLOGÍAS:
    • IDEs y editores de código preferidos
    • Plataformas de notebooks y desarrollo colaborativo
    • Herramientas de visualización de datos
    • Sistemas de bases de datos relacionales y NoSQL
    
    📈 ANÁLISIS DE TENDENCIAS:
    • Evolución de tecnologías en la industria
    • Preferencias de herramientas por región y experiencia
    • Tendencias salariales y de mercado laboral
    • Patrones de adopción de nuevas tecnologías
    
    🎯 APLICACIONES ESPECÍFICAS:
    • Diseño de arquitecturas de software escalables
    • Selección de tecnologías apropiadas para proyectos
    • Planificación de infraestructura de datos
    • Desarrollo de sistemas de machine learning
    • Implementación de pipelines de datos
    • Optimización de rendimiento de sistemas
    • Gestión de equipos de desarrollo
    • Toma de decisiones tecnológicas estratégicas
    """
    
    print(relevancia)

def main():
    """
    Función principal para ejecutar la visualización de extracción
    """
    print("🚀 VISUALIZACIÓN DE LA FASE DE EXTRACCIÓN")
    print("📊 Dataset: Kaggle Machine Learning & Data Science Survey 2019")
    print("🎯 Aplicación: Ingeniería de Sistemas")
    print("=" * 80)
    
    # Verificar archivo
    if not verificar_archivo():
        return
    
    # Extraer datos
    df = extraer_datos()
    if df is None:
        return
    
    # Mostrar información general
    mostrar_informacion_general(df)
    
    # Mostrar primeros registros
    mostrar_primeros_registros(df, 10)
    
    # Mostrar información de columnas principales
    mostrar_columnas_principales(df)
    
    # Mostrar estadísticas básicas
    mostrar_estadisticas_basicas(df)
    
    # Mostrar relevancia para Ingeniería de Sistemas
    mostrar_relevancia_ingenieria_sistemas()
    
    print("\n" + "=" * 80)
    print("✅ FASE DE EXTRACCIÓN COMPLETADA")
    print("📊 Dataset listo para la siguiente fase: TRANSFORMACIÓN")
    print("=" * 80)
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Ejecutar: python ver_transformacion_datos.py")
    print("2. Ejecutar: python ver_limpieza_datos.py")
    print("3. Ejecutar: python ver_carga_datos.py")
    print("4. O ejecutar todo: python ejecutar_proceso_completo.py")

if __name__ == "__main__":
    main()

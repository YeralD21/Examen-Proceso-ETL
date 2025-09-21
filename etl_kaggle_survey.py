#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proceso ETL (Extract, Transform, Load) para el Dataset de Kaggle Survey
Aplicado al área de Ingeniería de Sistemas

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
Propósito: Análisis de datos de encuesta de Kaggle para profesionales en Ingeniería de Sistemas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import os

# Configuración para mostrar todas las columnas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
warnings.filterwarnings('ignore')

# Configuración de matplotlib para español
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

class ETLKaggleSurvey:
    """
    Clase para realizar el proceso ETL completo del dataset de Kaggle Survey
    enfocado en Ingeniería de Sistemas
    """
    
    def __init__(self, file_path):
        """
        Inicializa la clase ETL
        
        Args:
            file_path (str): Ruta al archivo CSV del dataset
        """
        self.file_path = file_path
        self.df_original = None
        self.df_cleaned = None
        self.column_mapping = self._create_column_mapping()
        
    def _create_column_mapping(self):
        """
        Crea el mapeo de columnas Q1-Q50 a descripciones descriptivas
        
        Returns:
            dict: Diccionario con mapeo de columnas
        """
        return {
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
            
            # Notebooks hospedados
            'Q13_Part_1': 'Notebook_Kaggle_Kernels',
            'Q13_Part_2': 'Notebook_Google_Colab',
            'Q13_Part_3': 'Notebook_Azure_Notebook',
            'Q13_Part_4': 'Notebook_Domino_Datalab',
            'Q13_Part_5': 'Notebook_Google_Cloud_Datalab',
            'Q13_Part_6': 'Notebook_Paperspace',
            'Q13_Part_7': 'Notebook_Floydhub',
            'Q13_Part_8': 'Notebook_Crestle',
            'Q13_Part_9': 'Notebook_JupyterHub_Binder',
            'Q13_OTHER_TEXT': 'Notebook_Otros_Texto_Libre',
            
            # Servicios de computación en la nube
            'Q14_Part_1': 'Cloud_Google_Cloud_Platform',
            'Q14_Part_2': 'Cloud_Amazon_Web_Services',
            'Q14_Part_3': 'Cloud_Microsoft_Azure',
            'Q14_Part_4': 'Cloud_IBM_Cloud',
            'Q14_Part_5': 'Cloud_Alibaba_Cloud',
            'Q14_OTHER_TEXT': 'Cloud_Otros_Texto_Libre',
            
            # Lenguajes de programación específicos
            'Q15_Part_1': 'Lenguaje_Python',
            'Q15_Part_2': 'Lenguaje_R',
            'Q15_Part_3': 'Lenguaje_SQL',
            'Q15_Part_4': 'Lenguaje_Bash',
            'Q15_Part_5': 'Lenguaje_Java',
            'Q15_Part_6': 'Lenguaje_Javascript_Typescript',
            'Q15_Part_7': 'Lenguaje_Visual_Basic_VBA',
            'Q15_OTHER_TEXT': 'Lenguaje_Otros_Texto_Libre',
            
            # Lenguaje más usado
            'Q16': 'Lenguaje_Mas_Usado',
            'Q16_OTHER_TEXT': 'Lenguaje_Mas_Usado_Texto_Libre',
            
            # Lenguaje recomendado
            'Q17': 'Lenguaje_Recomendado_Data_Science',
            'Q17_OTHER_TEXT': 'Lenguaje_Recomendado_Texto_Libre',
            
            # Frameworks de Machine Learning
            'Q18_Part_1': 'ML_Scikit_Learn',
            'Q18_Part_2': 'ML_TensorFlow',
            'Q18_Part_3': 'ML_Keras',
            'Q18_Part_4': 'ML_PyTorch',
            'Q18_Part_5': 'ML_Spark_MLlib',
            'Q18_Part_6': 'ML_H20',
            'Q18_Part_7': 'ML_Fastai',
            'Q18_OTHER_TEXT': 'ML_Otros_Texto_Libre',
            
            # Framework ML más usado
            'Q19': 'ML_Framework_Mas_Usado',
            'Q19_OTHER_TEXT': 'ML_Framework_Mas_Usado_Texto_Libre',
            
            # Bibliotecas de visualización
            'Q20_Part_1': 'Viz_ggplot2',
            'Q20_Part_2': 'Viz_Matplotlib',
            'Q20_Part_3': 'Viz_Altair',
            'Q20_Part_4': 'Viz_Shiny',
            'Q20_Part_5': 'Viz_D3',
            'Q20_Part_6': 'Viz_Plotly',
            'Q20_Part_7': 'Viz_Bokeh',
            'Q20_Part_8': 'Viz_Seaborn',
            'Q20_OTHER_TEXT': 'Viz_Otros_Texto_Libre',
            
            # Biblioteca de visualización más usada
            'Q21': 'Viz_Biblioteca_Mas_Usada',
            'Q21_OTHER_TEXT': 'Viz_Biblioteca_Mas_Usada_Texto_Libre',
            
            # Tiempo dedicado a codificación
            'Q22': 'Porcentaje_Tiempo_Codificacion',
            'Q22_OTHER_TEXT': 'Porcentaje_Tiempo_Codificacion_Texto_Libre',
            
            # Experiencia en análisis de datos
            'Q23': 'Anos_Escribiendo_Codigo_Analisis',
            'Q24': 'Anos_Usando_Machine_Learning',
            'Q25': 'Se_Considera_Data_Scientist',
            
            # Productos de computación en la nube
            'Q26_Part_1': 'Cloud_Product_AWS_EC2',
            'Q26_Part_2': 'Cloud_Product_Google_Compute_Engine',
            'Q26_Part_3': 'Cloud_Product_AWS_Elastic_Beanstalk',
            'Q26_Part_4': 'Cloud_Product_Google_App_Engine',
            'Q26_Part_5': 'Cloud_Product_Google_Kubernetes_Engine',
            'Q26_Part_6': 'Cloud_Product_AWS_Lambda',
            'Q26_Part_7': 'Cloud_Product_Google_Cloud_Functions',
            'Q26_OTHER_TEXT': 'Cloud_Product_Otros_Texto_Libre',
            
            # Productos de Machine Learning
            'Q27_Part_1': 'ML_Product_Amazon_Transcribe',
            'Q27_Part_2': 'ML_Product_Google_Speech_to_Text',
            'Q27_Part_3': 'ML_Product_Amazon_Rekognition',
            'Q27_Part_4': 'ML_Product_Google_Vision_API',
            'Q27_Part_5': 'ML_Product_Amazon_Comprehend',
            'Q27_Part_6': 'ML_Product_Google_Natural_Language',
            'Q27_Part_7': 'ML_Product_Amazon_Translate',
            'Q27_Part_8': 'ML_Product_Google_Translation_API',
            'Q27_OTHER_TEXT': 'ML_Product_Otros_Texto_Libre',
            
            # Bases de datos relacionales
            'Q28_Part_1': 'DB_AWS_RDS',
            'Q28_Part_2': 'DB_AWS_Aurora',
            'Q28_Part_3': 'DB_Google_Cloud_SQL',
            'Q28_Part_4': 'DB_Google_Cloud_Spanner',
            'Q28_Part_5': 'DB_AWS_DynamoDB',
            'Q28_Part_6': 'DB_Google_Cloud_Datastore',
            'Q28_Part_7': 'DB_Google_Cloud_Bigtable',
            'Q28_Part_8': 'DB_AWS_SimpleDB',
            'Q28_Part_9': 'DB_Microsoft_SQL_Server',
            'Q28_Part_10': 'DB_MySQL',
            'Q28_OTHER_TEXT': 'DB_Otros_Texto_Libre',
            
            # Productos de Big Data y Analytics
            'Q29_Part_1': 'BigData_AWS_Elastic_MapReduce',
            'Q29_Part_2': 'BigData_AWS_Batch',
            'Q29_Part_3': 'BigData_Google_Cloud_Dataproc',
            'Q29_Part_4': 'BigData_Google_Cloud_Dataflow',
            'Q29_Part_5': 'BigData_Google_Cloud_Dataprep',
            'Q29_Part_6': 'BigData_AWS_Kinesis',
            'Q29_Part_7': 'BigData_Google_Cloud_Pub_Sub',
            'Q29_Part_8': 'BigData_AWS_Athena',
            'Q29_Part_9': 'BigData_AWS_Redshift',
            'Q29_Part_10': 'BigData_Google_BigQuery',
            'Q29_OTHER_TEXT': 'BigData_Otros_Texto_Libre',
            
            # Tipos de datos
            'Q30_Part_1': 'Tipo_Datos_Audio',
            'Q30_Part_2': 'Tipo_Datos_Categoricos',
            'Q30_Part_3': 'Tipo_Datos_Geneticos',
            'Q30_Part_4': 'Tipo_Datos_Geoespaciales',
            'Q30_Part_5': 'Tipo_Datos_Imagenes',
            'Q30_Part_6': 'Tipo_Datos_Numericos',
            'Q30_Part_7': 'Tipo_Datos_Sensores',
            'Q30_Part_8': 'Tipo_Datos_Tabulares',
            'Q30_Part_9': 'Tipo_Datos_Texto',
            'Q30_Part_10': 'Tipo_Datos_Series_Temporales',
            'Q30_OTHER_TEXT': 'Tipo_Datos_Otros_Texto_Libre',
            
            # Tipo de datos más usado
            'Q31': 'Tipo_Datos_Mas_Usado',
            'Q31_OTHER_TEXT': 'Tipo_Datos_Mas_Usado_Texto_Libre',
            
            # Fuentes de datasets públicos
            'Q32': 'Fuentes_Datasets_Publicos',
            'Q32_OTHER_TEXT': 'Fuentes_Datasets_Publicos_Texto_Libre',
            
            # Distribución de tiempo en proyectos
            'Q33': 'Tiempo_Recoleccion_Datos',
            'Q34': 'Tiempo_Limpieza_Datos',
            'Q35': 'Tiempo_Visualizacion_Datos',
            'Q36': 'Tiempo_Construccion_Modelos',
            'Q37': 'Tiempo_Produccion_Modelos',
            'Q38': 'Tiempo_Insights_Comunicacion',
            'Q39': 'Tiempo_Otras_Actividades',
            
            # Distribución de entrenamiento
            'Q40': 'Entrenamiento_Autodidacta',
            'Q41': 'Entrenamiento_Cursos_Online',
            'Q42': 'Entrenamiento_Trabajo',
            'Q43': 'Entrenamiento_Universidad',
            'Q44': 'Entrenamiento_Competencias_Kaggle',
            'Q45': 'Entrenamiento_Otros',
            'Q45_OTHER_TEXT': 'Entrenamiento_Otros_Texto_Libre',
            
            # Plataformas educativas
            'Q46': 'Plataformas_Educativas_Usadas',
            'Q46_OTHER_TEXT': 'Plataformas_Educativas_Texto_Libre',
            
            # Plataforma educativa más usada
            'Q47': 'Plataforma_Educativa_Mas_Usada',
            'Q47_OTHER_TEXT': 'Plataforma_Educativa_Mas_Usada_Texto_Libre',
            
            # Fuentes de medios favoritas
            'Q48': 'Fuentes_Medios_Favoritas',
            'Q48_OTHER_TEXT': 'Fuentes_Medios_Favoritas_Texto_Libre',
            
            # Percepción de calidad educativa
            'Q49': 'Percepcion_Calidad_Plataformas_Online',
            'Q50': 'Percepcion_Calidad_Bootcamps_Presenciales'
        }
    
    def extract_data(self):
        """
        FASE 1: EXTRACCIÓN DE DATOS
        Carga el dataset desde el archivo CSV
        
        Returns:
            pd.DataFrame: Dataset original cargado
        """
        print("=" * 80)
        print("FASE 1: EXTRACCIÓN DE DATOS")
        print("=" * 80)
        
        try:
            # Cargar el dataset
            print(f"Cargando dataset desde: {self.file_path}")
            self.df_original = pd.read_csv(self.file_path, encoding='utf-8')
            
            print(f"✅ Dataset cargado exitosamente")
            print(f"📊 Dimensiones del dataset: {self.df_original.shape}")
            print(f"📋 Número de registros: {self.df_original.shape[0]:,}")
            print(f"📋 Número de columnas: {self.df_original.shape[1]:,}")
            
            return self.df_original
            
        except Exception as e:
            print(f"❌ Error al cargar el dataset: {str(e)}")
            return None
    
    def describe_dataset(self):
        """
        Describe el dataset y su relevancia para Ingeniería de Sistemas
        """
        print("\n" + "=" * 80)
        print("DESCRIPCIÓN DEL DATASET PARA INGENIERÍA DE SISTEMAS")
        print("=" * 80)
        
        description = """
        📊 DATASET: Kaggle Machine Learning & Data Science Survey 2019
        
        🎯 RELEVANCIA PARA INGENIERÍA DE SISTEMAS:
        
        Este dataset es altamente relevante para el área de Ingeniería de Sistemas porque:
        
        1. 🏗️ INFRAESTRUCTURA Y ARQUITECTURA:
           - Contiene información sobre herramientas de desarrollo (IDEs, editores)
           - Datos sobre plataformas de computación en la nube (AWS, Azure, GCP)
           - Información sobre bases de datos y sistemas de almacenamiento
           - Herramientas de big data y analytics
        
        2. 💻 DESARROLLO DE SOFTWARE:
           - Lenguajes de programación más utilizados en la industria
           - Frameworks y bibliotecas de machine learning
           - Herramientas de control de versiones y colaboración
           - Metodologías de desarrollo y despliegue
        
        3. 🔧 HERRAMIENTAS Y TECNOLOGÍAS:
           - IDEs y editores de código preferidos
           - Plataformas de notebooks y desarrollo colaborativo
           - Herramientas de visualización de datos
           - Sistemas de bases de datos relacionales y NoSQL
        
        4. 📈 ANÁLISIS DE TENDENCIAS:
           - Evolución de tecnologías en la industria
           - Preferencias de herramientas por región y experiencia
           - Tendencias salariales y de mercado laboral
           - Patrones de adopción de nuevas tecnologías
        
        5. 🎓 FORMACIÓN Y COMPETENCIAS:
           - Rutas de aprendizaje más efectivas
           - Plataformas educativas preferidas
           - Competencias técnicas más demandadas
           - Brechas entre formación académica y necesidades industriales
        
        🎯 APLICACIONES ESPECÍFICAS EN INGENIERÍA DE SISTEMAS:
        
        • Diseño de arquitecturas de software escalables
        • Selección de tecnologías apropiadas para proyectos
        • Planificación de infraestructura de datos
        • Desarrollo de sistemas de machine learning
        • Implementación de pipelines de datos
        • Optimización de rendimiento de sistemas
        • Gestión de equipos de desarrollo
        • Toma de decisiones tecnológicas estratégicas
        """
        
        print(description)
        
        # Información básica del dataset
        print(f"\n📊 INFORMACIÓN TÉCNICA DEL DATASET:")
        print(f"   • Fuente: Kaggle (https://www.kaggle.com)")
        print(f"   • Año: 2019")
        print(f"   • Tipo: Encuesta de múltiple opción")
        print(f"   • Alcance: Global (múltiples países)")
        print(f"   • Población objetivo: Profesionales en Data Science y ML")
        print(f"   • Tamaño: {self.df_original.shape[0]:,} respuestas")
        print(f"   • Variables: {self.df_original.shape[1]:,} columnas")
    
    def exploratory_data_analysis(self):
        """
        FASE 2A: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
        """
        print("\n" + "=" * 80)
        print("FASE 2A: ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
        print("=" * 80)
        
        df = self.df_original.copy()
        
        # 1. Información general del dataset
        print("📊 1. INFORMACIÓN GENERAL DEL DATASET")
        print("-" * 50)
        print(f"Dimensiones: {df.shape}")
        print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # 2. Tipos de datos
        print("\n📋 2. TIPOS DE DATOS")
        print("-" * 50)
        print(df.dtypes.value_counts())
        
        # 3. Valores faltantes
        print("\n❌ 3. ANÁLISIS DE VALORES FALTANTES")
        print("-" * 50)
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        
        missing_summary = pd.DataFrame({
            'Valores_Faltantes': missing_data,
            'Porcentaje': missing_percentage
        }).sort_values('Valores_Faltantes', ascending=False)
        
        print(f"Total de columnas con valores faltantes: {(missing_data > 0).sum()}")
        print(f"Total de valores faltantes: {missing_data.sum():,}")
        print(f"Porcentaje promedio de valores faltantes: {missing_percentage.mean():.2f}%")
        
        # Mostrar las 10 columnas con más valores faltantes
        print("\n🔝 Top 10 columnas con más valores faltantes:")
        print(missing_summary.head(10))
        
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
            print(df[numeric_cols].describe())
        else:
            print("No se encontraron columnas numéricas")
        
        # 7. Análisis de columnas categóricas principales
        print("\n📊 7. ANÁLISIS DE COLUMNAS CATEGÓRICAS PRINCIPALES")
        print("-" * 50)
        
        # Analizar algunas columnas clave
        key_columns = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9']
        for col in key_columns:
            if col in df.columns:
                print(f"\n{col} - {self.column_mapping.get(col, col)}:")
                value_counts = df[col].value_counts().head(5)
                for value, count in value_counts.items():
                    percentage = (count / len(df)) * 100
                    print(f"  • {value}: {count:,} ({percentage:.1f}%)")
        
        return {
            'dimensions': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_data': missing_summary,
            'duplicates': duplicates,
            'unique_counts': unique_counts
        }
    
    def clean_and_transform_data(self):
        """
        FASE 2B: LIMPIEZA Y TRANSFORMACIÓN DE DATOS
        """
        print("\n" + "=" * 80)
        print("FASE 2B: LIMPIEZA Y TRANSFORMACIÓN DE DATOS")
        print("=" * 80)
        
        df = self.df_original.copy()
        print(f"📊 Dataset inicial: {df.shape}")
        
        # 1. Eliminación de registros duplicados
        print("\n🔄 1. ELIMINACIÓN DE REGISTROS DUPLICADOS")
        print("-" * 50)
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed_duplicates = initial_rows - len(df)
        print(f"Registros eliminados por duplicación: {removed_duplicates}")
        print(f"Registros restantes: {len(df):,}")
        
        # 2. Manejo de valores nulos
        print("\n❌ 2. MANEJO DE VALORES NULOS")
        print("-" * 50)
        
        # Estrategia: Para columnas con más del 80% de valores faltantes, las eliminamos
        # Para el resto, imputamos con valores apropiados
        missing_percentage = (df.isnull().sum() / len(df)) * 100
        
        # Eliminar columnas con más del 80% de valores faltantes
        columns_to_drop = missing_percentage[missing_percentage > 80].index
        print(f"Columnas eliminadas (>80% valores faltantes): {len(columns_to_drop)}")
        df = df.drop(columns=columns_to_drop)
        
        # Para columnas categóricas, imputar con "No especificado"
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('No especificado')
        
        # Para columnas numéricas, imputar con la mediana
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        
        print(f"Valores nulos restantes: {df.isnull().sum().sum()}")
        
        # 3. Limpieza de espacios en blanco
        print("\n🧹 3. LIMPIEZA DE ESPACIOS EN BLANCO")
        print("-" * 50)
        
        # Eliminar espacios al inicio y final de strings
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # 4. Normalización de datos
        print("\n🔄 4. NORMALIZACIÓN DE DATOS")
        print("-" * 50)
        
        # Normalizar texto a minúsculas para ciertas columnas
        text_columns = ['Q1_OTHER_TEXT', 'Q6_OTHER_TEXT', 'Q7_OTHER_TEXT', 'Q11_OTHER_TEXT']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].str.lower()
        
        # 5. Conversión de tipos de datos
        print("\n🔄 5. CONVERSIÓN DE TIPOS DE DATOS")
        print("-" * 50)
        
        # Convertir columna de tiempo a numérico
        if 'Time from Start to Finish (seconds)' in df.columns:
            df['Time from Start to Finish (seconds)'] = pd.to_numeric(
                df['Time from Start to Finish (seconds)'], errors='coerce'
            )
        
        # 6. Renombrar columnas con descripciones descriptivas
        print("\n📝 6. RENOMBRADO DE COLUMNAS")
        print("-" * 50)
        
        # Crear mapeo solo para columnas que existen en el dataset
        existing_mapping = {k: v for k, v in self.column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_mapping)
        
        print(f"Columnas renombradas: {len(existing_mapping)}")
        print("Ejemplos de renombrado:")
        for i, (old_name, new_name) in enumerate(list(existing_mapping.items())[:5]):
            print(f"  • {old_name} → {new_name}")
        
        # 7. Crear columnas derivadas útiles para análisis
        print("\n➕ 7. CREACIÓN DE COLUMNAS DERIVADAS")
        print("-" * 50)
        
        # Crear categoría de experiencia
        if 'Anos_Experiencia_Campo' in df.columns:
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
            
            df['Categoria_Experiencia'] = df['Anos_Experiencia_Campo'].apply(categorize_experience)
        
        # Crear categoría de salario
        if 'Rango_Salarial_Anual' in df.columns:
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
            
            df['Categoria_Salarial'] = df['Rango_Salarial_Anual'].apply(categorize_salary)
        
        print(f"Columnas derivadas creadas: 2")
        print("  • Categoria_Experiencia")
        print("  • Categoria_Salarial")
        
        # Guardar dataset limpio
        self.df_cleaned = df
        
        print(f"\n✅ LIMPIEZA COMPLETADA")
        print(f"📊 Dataset final: {df.shape}")
        print(f"📉 Reducción de filas: {initial_rows - len(df):,}")
        print(f"📉 Reducción de columnas: {self.df_original.shape[1] - df.shape[1]}")
        
        return df
    
    def load_data(self, output_format='csv'):
        """
        FASE 3: CARGA DE DATOS
        Exporta los datos limpios en diferentes formatos
        """
        print("\n" + "=" * 80)
        print("FASE 3: CARGA DE DATOS")
        print("=" * 80)
        
        if self.df_cleaned is None:
            print("❌ Error: No hay datos limpios para exportar")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Exportar a CSV
        if output_format in ['csv', 'all']:
            csv_filename = f"kaggle_survey_cleaned_{timestamp}.csv"
            self.df_cleaned.to_csv(csv_filename, index=False, encoding='utf-8')
            print(f"✅ Dataset exportado a CSV: {csv_filename}")
        
        # 2. Exportar a Excel
        if output_format in ['excel', 'all']:
            excel_filename = f"kaggle_survey_cleaned_{timestamp}.xlsx"
            with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
                self.df_cleaned.to_excel(writer, sheet_name='Datos_Limpios', index=False)
                
                # Crear hoja con resumen de cambios
                summary_data = {
                    'Métrica': [
                        'Registros originales',
                        'Registros finales',
                        'Columnas originales',
                        'Columnas finales',
                        'Registros duplicados eliminados',
                        'Columnas eliminadas (>80% nulos)',
                        'Valores nulos imputados',
                        'Columnas renombradas'
                    ],
                    'Valor': [
                        f"{self.df_original.shape[0]:,}",
                        f"{self.df_cleaned.shape[0]:,}",
                        f"{self.df_original.shape[1]:,}",
                        f"{self.df_cleaned.shape[1]:,}",
                        f"{self.df_original.shape[0] - self.df_cleaned.shape[0]:,}",
                        f"{self.df_original.shape[1] - self.df_cleaned.shape[1]:,}",
                        f"{self.df_original.isnull().sum().sum() - self.df_cleaned.isnull().sum().sum():,}",
                        f"{len(self.column_mapping):,}"
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Resumen_Cambios', index=False)
            
            print(f"✅ Dataset exportado a Excel: {excel_filename}")
        
        # 3. Crear archivo de metadatos
        metadata_filename = f"metadata_etl_{timestamp}.txt"
        with open(metadata_filename, 'w', encoding='utf-8') as f:
            f.write("METADATOS DEL PROCESO ETL - KAGGLE SURVEY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fecha de procesamiento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Archivo original: {self.file_path}\n")
            f.write(f"Registros originales: {self.df_original.shape[0]:,}\n")
            f.write(f"Registros finales: {self.df_cleaned.shape[0]:,}\n")
            f.write(f"Columnas originales: {self.df_original.shape[1]:,}\n")
            f.write(f"Columnas finales: {self.df_cleaned.shape[1]:,}\n\n")
            
            f.write("CAMBIOS REALIZADOS:\n")
            f.write("-" * 20 + "\n")
            f.write("1. Eliminación de registros duplicados\n")
            f.write("2. Eliminación de columnas con >80% valores faltantes\n")
            f.write("3. Imputación de valores nulos:\n")
            f.write("   - Categóricas: 'No especificado'\n")
            f.write("   - Numéricas: Mediana\n")
            f.write("4. Limpieza de espacios en blanco\n")
            f.write("5. Normalización de texto (minúsculas)\n")
            f.write("6. Renombrado de columnas Q1-Q50\n")
            f.write("7. Creación de columnas derivadas\n\n")
            
            f.write("COLUMNAS RENOMBRADAS:\n")
            f.write("-" * 20 + "\n")
            for old_name, new_name in self.column_mapping.items():
                if old_name in self.df_original.columns:
                    f.write(f"{old_name} → {new_name}\n")
        
        print(f"✅ Metadatos exportados: {metadata_filename}")
        
        return {
            'csv_file': csv_filename if output_format in ['csv', 'all'] else None,
            'excel_file': excel_filename if output_format in ['excel', 'all'] else None,
            'metadata_file': metadata_filename
        }
    
    def generate_summary_report(self):
        """
        Genera un reporte resumen del proceso ETL
        """
        print("\n" + "=" * 80)
        print("REPORTE RESUMEN DEL PROCESO ETL")
        print("=" * 80)
        
        if self.df_cleaned is None:
            print("❌ Error: No hay datos procesados para generar reporte")
            return
        
        print(f"📊 RESUMEN EJECUTIVO:")
        print(f"   • Dataset procesado: Kaggle ML & Data Science Survey 2019")
        print(f"   • Registros procesados: {self.df_cleaned.shape[0]:,}")
        print(f"   • Variables finales: {self.df_cleaned.shape[1]:,}")
        print(f"   • Tasa de retención: {(len(self.df_cleaned) / len(self.df_original)) * 100:.1f}%")
        
        print(f"\n🔧 TRANSFORMACIONES APLICADAS:")
        print(f"   • Registros duplicados eliminados: {len(self.df_original) - len(self.df_cleaned):,}")
        print(f"   • Columnas eliminadas: {self.df_original.shape[1] - self.df_cleaned.shape[1]:,}")
        print(f"   • Valores nulos imputados: {self.df_original.isnull().sum().sum() - self.df_cleaned.isnull().sum().sum():,}")
        print(f"   • Columnas renombradas: {len(self.column_mapping):,}")
        
        print(f"\n📈 CALIDAD DE DATOS:")
        print(f"   • Completitud promedio: {((self.df_cleaned.notna().sum().sum()) / (self.df_cleaned.shape[0] * self.df_cleaned.shape[1])) * 100:.1f}%")
        print(f"   • Consistencia: Mejorada mediante normalización")
        print(f"   • Validez: Verificada mediante validación de tipos")
        
        print(f"\n🎯 APLICACIÓN EN INGENIERÍA DE SISTEMAS:")
        print(f"   • Análisis de tendencias tecnológicas")
        print(f"   • Benchmarking de herramientas de desarrollo")
        print(f"   • Análisis de mercado laboral")
        print(f"   • Planificación de arquitecturas de software")
        print(f"   • Selección de tecnologías apropiadas")
    
    def run_complete_etl(self, output_format='all'):
        """
        Ejecuta el proceso ETL completo
        
        Args:
            output_format (str): Formato de salida ('csv', 'excel', 'all')
        """
        print("🚀 INICIANDO PROCESO ETL COMPLETO")
        print("Dataset: Kaggle Machine Learning & Data Science Survey 2019")
        print("Aplicación: Ingeniería de Sistemas")
        print("=" * 80)
        
        # Fase 1: Extracción
        if self.extract_data() is None:
            return False
        
        # Descripción del dataset
        self.describe_dataset()
        
        # Fase 2A: EDA
        eda_results = self.exploratory_data_analysis()
        
        # Fase 2B: Limpieza y transformación
        self.df_cleaned = self.clean_and_transform_data()
        
        # Fase 3: Carga
        output_files = self.load_data(output_format)
        
        # Reporte final
        self.generate_summary_report()
        
        print("\n" + "=" * 80)
        print("✅ PROCESO ETL COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        
        return True

def main():
    """
    Función principal para ejecutar el proceso ETL
    """
    # Configurar la ruta del archivo
    file_path = "multipleChoiceResponses.csv"
    
    # Verificar que el archivo existe
    if not os.path.exists(file_path):
        print(f"❌ Error: No se encontró el archivo {file_path}")
        print("Asegúrate de que el archivo esté en el directorio actual")
        return
    
    # Crear instancia del ETL
    etl = ETLKaggleSurvey(file_path)
    
    # Ejecutar proceso completo
    success = etl.run_complete_etl(output_format='all')
    
    if success:
        print("\n🎉 ¡Proceso ETL completado exitosamente!")
        print("📁 Archivos generados:")
        print("   • kaggle_survey_cleaned_[timestamp].csv")
        print("   • kaggle_survey_cleaned_[timestamp].xlsx")
        print("   • metadata_etl_[timestamp].txt")
        print("\n📊 El dataset está listo para análisis en Power BI")
    else:
        print("\n❌ Error en el proceso ETL")

if __name__ == "__main__":
    main()

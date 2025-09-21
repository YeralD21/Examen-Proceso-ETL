#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis y Visualizaciones para el Dataset de Kaggle Survey
Enfoque en Ingeniería de Sistemas

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Configuración para matplotlib
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

class AnalisisVisualizaciones:
    """
    Clase para generar análisis y visualizaciones del dataset de Kaggle Survey
    enfocado en Ingeniería de Sistemas
    """
    
    def __init__(self, df_cleaned):
        """
        Inicializa la clase con el dataset limpio
        
        Args:
            df_cleaned (pd.DataFrame): Dataset limpio del proceso ETL
        """
        self.df = df_cleaned
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def analisis_demografico(self):
        """
        Análisis demográfico de los encuestados
        """
        print("📊 ANÁLISIS DEMOGRÁFICO")
        print("=" * 50)
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))
        fig.suptitle('Análisis Demográfico - Kaggle Survey 2019', fontsize=20, fontweight='bold')
        
        # 1. Distribución por edad
        if 'Edad_Encuestado' in self.df.columns:
            age_counts = self.df['Edad_Encuestado'].value_counts()
            axes[0, 0].pie(age_counts.values, labels=age_counts.index, autopct='%1.1f%%', 
                          colors=self.colors[:len(age_counts)])
            axes[0, 0].set_title('Distribución por Edad', fontweight='bold')
        
        # 2. Distribución por género
        if 'Genero' in self.df.columns:
            gender_counts = self.df['Genero'].value_counts()
            axes[0, 1].bar(gender_counts.index, gender_counts.values, color=self.colors[:len(gender_counts)])
            axes[0, 1].set_title('Distribución por Género', fontweight='bold')
            axes[0, 1].set_ylabel('Número de Encuestados')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Distribución por nivel educativo
        if 'Nivel_Educativo' in self.df.columns:
            edu_counts = self.df['Nivel_Educativo'].value_counts()
            axes[1, 0].barh(edu_counts.index, edu_counts.values, color=self.colors[:len(edu_counts)])
            axes[1, 0].set_title('Distribución por Nivel Educativo', fontweight='bold')
            axes[1, 0].set_xlabel('Número de Encuestados')
        
        # 4. Top 10 países
        if 'Pais_Residencia' in self.df.columns:
            country_counts = self.df['Pais_Residencia'].value_counts().head(10)
            axes[1, 1].barh(country_counts.index, country_counts.values, color=self.colors[:len(country_counts)])
            axes[1, 1].set_title('Top 10 Países', fontweight='bold')
            axes[1, 1].set_xlabel('Número de Encuestados')
        
        plt.tight_layout()
        plt.savefig('analisis_demografico.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas demográficas
        print(f"Total de encuestados: {len(self.df):,}")
        if 'Genero' in self.df.columns:
            print(f"Distribución por género:")
            for gender, count in self.df['Genero'].value_counts().items():
                percentage = (count / len(self.df)) * 100
                print(f"  • {gender}: {count:,} ({percentage:.1f}%)")
    
    def analisis_lenguajes_programacion(self):
        """
        Análisis de lenguajes de programación más utilizados
        """
        print("\n💻 ANÁLISIS DE LENGUAJES DE PROGRAMACIÓN")
        print("=" * 50)
        
        # Identificar columnas de lenguajes de programación
        lang_columns = [col for col in self.df.columns if col.startswith('Lenguaje_') and col != 'Lenguaje_Otros_Texto_Libre']
        
        if not lang_columns:
            print("No se encontraron columnas de lenguajes de programación")
            return
        
        # Contar uso de cada lenguaje
        lang_usage = {}
        for col in lang_columns:
            lang_name = col.replace('Lenguaje_', '').replace('_', ' ')
            count = self.df[col].notna().sum()
            lang_usage[lang_name] = count
        
        # Ordenar por uso
        lang_usage = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True))
        
        # Crear visualización
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('Análisis de Lenguajes de Programación', fontsize=18, fontweight='bold')
        
        # Gráfico de barras
        languages = list(lang_usage.keys())[:10]  # Top 10
        counts = list(lang_usage.values())[:10]
        
        bars = ax1.bar(languages, counts, color=self.colors[:len(languages)])
        ax1.set_title('Top 10 Lenguajes de Programación', fontweight='bold')
        ax1.set_ylabel('Número de Usuarios')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 100,
                    f'{count:,}', ha='center', va='bottom')
        
        # Gráfico de pastel para top 5
        top5_langs = list(lang_usage.keys())[:5]
        top5_counts = list(lang_usage.values())[:5]
        others_count = sum(list(lang_usage.values())[5:])
        
        if others_count > 0:
            top5_langs.append('Otros')
            top5_counts.append(others_count)
        
        ax2.pie(top5_counts, labels=top5_langs, autopct='%1.1f%%', 
                colors=self.colors[:len(top5_langs)])
        ax2.set_title('Distribución Top 5 + Otros', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('analisis_lenguajes_programacion.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas
        print("Top 10 lenguajes de programación:")
        for i, (lang, count) in enumerate(list(lang_usage.items())[:10], 1):
            percentage = (count / len(self.df)) * 100
            print(f"  {i:2d}. {lang}: {count:,} usuarios ({percentage:.1f}%)")
    
    def analisis_herramientas_desarrollo(self):
        """
        Análisis de herramientas de desarrollo (IDEs, editores)
        """
        print("\n🔧 ANÁLISIS DE HERRAMIENTAS DE DESARROLLO")
        print("=" * 50)
        
        # Identificar columnas de IDEs
        ide_columns = [col for col in self.df.columns if col.startswith('IDE_') and col != 'IDE_Otros_Texto_Libre']
        
        if not ide_columns:
            print("No se encontraron columnas de IDEs")
            return
        
        # Contar uso de cada IDE
        ide_usage = {}
        for col in ide_columns:
            ide_name = col.replace('IDE_', '').replace('_', ' ')
            count = self.df[col].notna().sum()
            ide_usage[ide_name] = count
        
        # Ordenar por uso
        ide_usage = dict(sorted(ide_usage.items(), key=lambda x: x[1], reverse=True))
        
        # Crear visualización
        fig, ax = plt.subplots(figsize=(15, 10))
        
        ides = list(ide_usage.keys())
        counts = list(ide_usage.values())
        
        bars = ax.barh(ides, counts, color=self.colors[:len(ides)])
        ax.set_title('Uso de IDEs y Editores de Código', fontsize=16, fontweight='bold')
        ax.set_xlabel('Número de Usuarios')
        
        # Agregar valores en las barras
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax.text(width + 50, bar.get_y() + bar.get_height()/2.,
                   f'{count:,}', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('analisis_herramientas_desarrollo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas
        print("Uso de IDEs y editores:")
        for i, (ide, count) in enumerate(ide_usage.items(), 1):
            percentage = (count / len(self.df)) * 100
            print(f"  {i:2d}. {ide}: {count:,} usuarios ({percentage:.1f}%)")
    
    def analisis_cloud_platforms(self):
        """
        Análisis de plataformas de computación en la nube
        """
        print("\n☁️ ANÁLISIS DE PLATAFORMAS DE NUBE")
        print("=" * 50)
        
        # Identificar columnas de cloud
        cloud_columns = [col for col in self.df.columns if col.startswith('Cloud_') and col != 'Cloud_Otros_Texto_Libre']
        
        if not cloud_columns:
            print("No se encontraron columnas de plataformas de nube")
            return
        
        # Contar uso de cada plataforma
        cloud_usage = {}
        for col in cloud_columns:
            cloud_name = col.replace('Cloud_', '').replace('_', ' ')
            count = self.df[col].notna().sum()
            cloud_usage[cloud_name] = count
        
        # Ordenar por uso
        cloud_usage = dict(sorted(cloud_usage.items(), key=lambda x: x[1], reverse=True))
        
        # Crear visualización
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('Análisis de Plataformas de Computación en la Nube', fontsize=18, fontweight='bold')
        
        # Gráfico de barras
        platforms = list(cloud_usage.keys())
        counts = list(cloud_usage.values())
        
        bars = ax1.bar(platforms, counts, color=self.colors[:len(platforms)])
        ax1.set_title('Uso de Plataformas de Nube', fontweight='bold')
        ax1.set_ylabel('Número de Usuarios')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{count:,}', ha='center', va='bottom')
        
        # Gráfico de pastel
        ax2.pie(counts, labels=platforms, autopct='%1.1f%%', 
                colors=self.colors[:len(platforms)])
        ax2.set_title('Distribución de Plataformas de Nube', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('analisis_cloud_platforms.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas
        print("Uso de plataformas de nube:")
        for i, (platform, count) in enumerate(cloud_usage.items(), 1):
            percentage = (count / len(self.df)) * 100
            print(f"  {i:2d}. {platform}: {count:,} usuarios ({percentage:.1f}%)")
    
    def analisis_salarios_experiencia(self):
        """
        Análisis de salarios vs experiencia
        """
        print("\n💰 ANÁLISIS DE SALARIOS Y EXPERIENCIA")
        print("=" * 50)
        
        # Verificar que las columnas necesarias existen
        if 'Categoria_Salarial' not in self.df.columns or 'Categoria_Experiencia' not in self.df.columns:
            print("No se encontraron las columnas de categorías de salario y experiencia")
            return
        
        # Crear tabla de contingencia
        salary_exp_cross = pd.crosstab(self.df['Categoria_Experiencia'], 
                                     self.df['Categoria_Salarial'], 
                                     normalize='index') * 100
        
        # Crear heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        sns.heatmap(salary_exp_cross, annot=True, fmt='.1f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Porcentaje (%)'}, ax=ax)
        
        ax.set_title('Relación entre Experiencia y Salario\n(Porcentaje por nivel de experiencia)', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel('Categoría Salarial')
        ax.set_ylabel('Categoría de Experiencia')
        
        plt.tight_layout()
        plt.savefig('analisis_salarios_experiencia.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas adicionales
        print("Distribución de salarios por experiencia:")
        for exp_level in self.df['Categoria_Experiencia'].unique():
            if exp_level != 'No especificado':
                exp_data = self.df[self.df['Categoria_Experiencia'] == exp_level]
                salary_dist = exp_data['Categoria_Salarial'].value_counts()
                print(f"\n{exp_level}:")
                for salary, count in salary_dist.items():
                    percentage = (count / len(exp_data)) * 100
                    print(f"  • {salary}: {count:,} ({percentage:.1f}%)")
    
    def analisis_areas_estudio(self):
        """
        Análisis de áreas de estudio y su relación con roles
        """
        print("\n🎓 ANÁLISIS DE ÁREAS DE ESTUDIO")
        print("=" * 50)
        
        if 'Area_Estudios_Principal' not in self.df.columns or 'Cargo_Principal_Trabajo' not in self.df.columns:
            print("No se encontraron las columnas de área de estudios y cargo")
            return
        
        # Top áreas de estudio
        area_counts = self.df['Area_Estudios_Principal'].value_counts().head(10)
        
        # Crear visualización
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('Análisis de Áreas de Estudio', fontsize=18, fontweight='bold')
        
        # Gráfico de barras
        areas = area_counts.index
        counts = area_counts.values
        
        bars = ax1.barh(areas, counts, color=self.colors[:len(areas)])
        ax1.set_title('Top 10 Áreas de Estudio', fontweight='bold')
        ax1.set_xlabel('Número de Encuestados')
        
        # Agregar valores en las barras
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax1.text(width + 50, bar.get_y() + bar.get_height()/2.,
                   f'{count:,}', ha='left', va='center')
        
        # Relación área de estudio vs cargo
        area_role_cross = pd.crosstab(self.df['Area_Estudios_Principal'], 
                                    self.df['Cargo_Principal_Trabajo'])
        
        # Seleccionar solo los cargos más comunes
        top_roles = self.df['Cargo_Principal_Trabajo'].value_counts().head(5).index
        area_role_subset = area_role_cross[top_roles]
        
        # Crear heatmap
        sns.heatmap(area_role_subset, annot=True, fmt='d', cmap='Blues', 
                   cbar_kws={'label': 'Número de Personas'}, ax=ax2)
        
        ax2.set_title('Área de Estudio vs Cargo Principal', fontweight='bold')
        ax2.set_xlabel('Cargo Principal')
        ax2.set_ylabel('Área de Estudio')
        
        plt.tight_layout()
        plt.savefig('analisis_areas_estudio.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Estadísticas
        print("Top 10 áreas de estudio:")
        for i, (area, count) in enumerate(area_counts.items(), 1):
            percentage = (count / len(self.df)) * 100
            print(f"  {i:2d}. {area}: {count:,} ({percentage:.1f}%)")
    
    def generar_reporte_completo(self):
        """
        Genera un reporte completo con todas las visualizaciones
        """
        print("🚀 GENERANDO REPORTE COMPLETO DE ANÁLISIS")
        print("=" * 60)
        
        # Ejecutar todos los análisis
        self.analisis_demografico()
        self.analisis_lenguajes_programacion()
        self.analisis_herramientas_desarrollo()
        self.analisis_cloud_platforms()
        self.analisis_salarios_experiencia()
        self.analisis_areas_estudio()
        
        print("\n✅ REPORTE COMPLETO GENERADO")
        print("📁 Archivos de visualización creados:")
        print("   • analisis_demografico.png")
        print("   • analisis_lenguajes_programacion.png")
        print("   • analisis_herramientas_desarrollo.png")
        print("   • analisis_cloud_platforms.png")
        print("   • analisis_salarios_experiencia.png")
        print("   • analisis_areas_estudio.png")
        
        # Crear resumen ejecutivo
        self.crear_resumen_ejecutivo()
    
    def crear_resumen_ejecutivo(self):
        """
        Crea un resumen ejecutivo del análisis
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumen_ejecutivo_analisis_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RESUMEN EJECUTIVO - ANÁLISIS KAGGLE SURVEY 2019\n")
            f.write("Enfoque: Ingeniería de Sistemas\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de encuestados analizados: {len(self.df):,}\n\n")
            
            f.write("HALLAZGOS PRINCIPALES:\n")
            f.write("-" * 30 + "\n\n")
            
            # Demografía
            if 'Genero' in self.df.columns:
                gender_dist = self.df['Genero'].value_counts()
                f.write("1. DEMOGRAFÍA:\n")
                for gender, count in gender_dist.items():
                    percentage = (count / len(self.df)) * 100
                    f.write(f"   • {gender}: {percentage:.1f}%\n")
                f.write("\n")
            
            # Lenguajes de programación
            lang_columns = [col for col in self.df.columns if col.startswith('Lenguaje_') and col != 'Lenguaje_Otros_Texto_Libre']
            if lang_columns:
                f.write("2. LENGUAJES DE PROGRAMACIÓN MÁS USADOS:\n")
                lang_usage = {}
                for col in lang_columns:
                    lang_name = col.replace('Lenguaje_', '').replace('_', ' ')
                    count = self.df[col].notna().sum()
                    lang_usage[lang_name] = count
                
                lang_usage = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True))
                for i, (lang, count) in enumerate(list(lang_usage.items())[:5], 1):
                    percentage = (count / len(self.df)) * 100
                    f.write(f"   {i}. {lang}: {percentage:.1f}%\n")
                f.write("\n")
            
            # Plataformas de nube
            cloud_columns = [col for col in self.df.columns if col.startswith('Cloud_') and col != 'Cloud_Otros_Texto_Libre']
            if cloud_columns:
                f.write("3. PLATAFORMAS DE NUBE MÁS USADAS:\n")
                cloud_usage = {}
                for col in cloud_columns:
                    cloud_name = col.replace('Cloud_', '').replace('_', ' ')
                    count = self.df[col].notna().sum()
                    cloud_usage[cloud_name] = count
                
                cloud_usage = dict(sorted(cloud_usage.items(), key=lambda x: x[1], reverse=True))
                for i, (platform, count) in enumerate(list(cloud_usage.items())[:3], 1):
                    percentage = (count / len(self.df)) * 100
                    f.write(f"   {i}. {platform}: {percentage:.1f}%\n")
                f.write("\n")
            
            f.write("RECOMENDACIONES PARA INGENIERÍA DE SISTEMAS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. Enfocar la formación en los lenguajes de programación más demandados\n")
            f.write("2. Incluir capacitación en las principales plataformas de nube\n")
            f.write("3. Desarrollar competencias en herramientas de desarrollo modernas\n")
            f.write("4. Considerar las tendencias salariales por nivel de experiencia\n")
            f.write("5. Adaptar el currículo según las áreas de estudio más relevantes\n")
        
        print(f"📄 Resumen ejecutivo creado: {filename}")

def main():
    """
    Función principal para ejecutar el análisis
    """
    # Cargar el dataset limpio
    try:
        # Buscar el archivo CSV más reciente
        import glob
        csv_files = glob.glob("kaggle_survey_cleaned_*.csv")
        if not csv_files:
            print("❌ No se encontró el archivo de dataset limpio")
            print("Ejecuta primero el script etl_kaggle_survey.py")
            return
        
        # Usar el archivo más reciente
        latest_file = max(csv_files, key=os.path.getctime)
        print(f"📁 Cargando dataset limpio: {latest_file}")
        
        df_cleaned = pd.read_csv(latest_file)
        
        # Crear instancia del analizador
        analyzer = AnalisisVisualizaciones(df_cleaned)
        
        # Generar reporte completo
        analyzer.generar_reporte_completo()
        
    except Exception as e:
        print(f"❌ Error al ejecutar el análisis: {str(e)}")

if __name__ == "__main__":
    import os
    main()

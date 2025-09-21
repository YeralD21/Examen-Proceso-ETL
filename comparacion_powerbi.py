#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Comparación con Power BI
Valida que los resultados del proceso ETL en Python sean replicables en Power BI

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class ComparacionPowerBI:
    """
    Clase para comparar y validar resultados entre Python y Power BI
    """
    
    def __init__(self, df_cleaned):
        """
        Inicializa la clase con el dataset limpio
        
        Args:
            df_cleaned (pd.DataFrame): Dataset limpio del proceso ETL
        """
        self.df = df_cleaned
        self.resultados_python = {}
        self.resultados_powerbi = {}
    
    def calcular_metricas_python(self):
        """
        Calcula las métricas principales en Python para comparación
        """
        print("📊 CALCULANDO MÉTRICAS EN PYTHON")
        print("=" * 50)
        
        # Métricas básicas
        self.resultados_python = {
            'total_registros': len(self.df),
            'total_columnas': len(self.df.columns),
            'valores_nulos_totales': self.df.isnull().sum().sum(),
            'registros_unicos': len(self.df.drop_duplicates()),
            'memoria_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Métricas por columnas específicas
        if 'Genero' in self.df.columns:
            self.resultados_python['distribucion_genero'] = self.df['Genero'].value_counts().to_dict()
        
        if 'Edad_Encuestado' in self.df.columns:
            self.resultados_python['distribucion_edad'] = self.df['Edad_Encuestado'].value_counts().to_dict()
        
        if 'Pais_Residencia' in self.df.columns:
            self.resultados_python['top_5_paises'] = self.df['Pais_Residencia'].value_counts().head(5).to_dict()
        
        if 'Nivel_Educativo' in self.df.columns:
            self.resultados_python['distribucion_educacion'] = self.df['Nivel_Educativo'].value_counts().to_dict()
        
        # Métricas de lenguajes de programación
        lang_columns = [col for col in self.df.columns if col.startswith('Lenguaje_') and col != 'Lenguaje_Otros_Texto_Libre']
        if lang_columns:
            lang_usage = {}
            for col in lang_columns:
                lang_name = col.replace('Lenguaje_', '').replace('_', ' ')
                count = self.df[col].notna().sum()
                lang_usage[lang_name] = count
            self.resultados_python['lenguajes_programacion'] = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True))
        
        # Métricas de plataformas de nube
        cloud_columns = [col for col in self.df.columns if col.startswith('Cloud_') and col != 'Cloud_Otros_Texto_Libre']
        if cloud_columns:
            cloud_usage = {}
            for col in cloud_columns:
                cloud_name = col.replace('Cloud_', '').replace('_', ' ')
                count = self.df[col].notna().sum()
                cloud_usage[cloud_name] = count
            self.resultados_python['plataformas_nube'] = dict(sorted(cloud_usage.items(), key=lambda x: x[1], reverse=True))
        
        print("✅ Métricas calculadas en Python")
        return self.resultados_python
    
    def generar_script_powerbi(self):
        """
        Genera un script de Power Query M para replicar el proceso ETL
        """
        print("\n🔧 GENERANDO SCRIPT DE POWER BI")
        print("=" * 50)
        
        script_powerbi = """
// Script de Power Query M para replicar el proceso ETL
// Kaggle Survey 2019 - Ingeniería de Sistemas

let
    // PASO 1: Cargar datos desde CSV
    Source = Csv.Document(File.Contents("multipleChoiceResponses.csv"),[Delimiter=",", Columns=350, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // PASO 2: Eliminar registros duplicados
    RemovedDuplicates = Table.Distinct(PromotedHeaders),
    
    // PASO 3: Manejo de valores nulos
    // Eliminar columnas con más del 80% de valores faltantes
    ColumnCount = Table.ColumnCount(RemovedDuplicates),
    RowCount = Table.RowCount(RemovedDuplicates),
    Threshold = RowCount * 0.8,
    
    // Identificar columnas a eliminar
    ColumnsToRemove = List.Select(Table.ColumnNames(RemovedDuplicates), 
        each List.Count(List.RemoveNulls(Table.Column(RemovedDuplicates, _))) < Threshold),
    
    // Eliminar columnas con muchos valores faltantes
    RemovedHighNullColumns = Table.RemoveColumns(RemovedDuplicates, ColumnsToRemove),
    
    // PASO 4: Imputar valores nulos
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
    TrimmedColumns = List.Accumulate(TextColumns, ImputedNumericColumns, 
        (table, column) => Table.TransformColumns(table, {{column, Text.Trim}})),
    
    // PASO 6: Renombrar columnas principales
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
            f.write(f"Total de registros: {self.resultados_python.get('total_registros', 'N/A')}\n")
            f.write(f"Total de columnas: {self.resultados_python.get('total_columnas', 'N/A')}\n")
            f.write(f"Valores nulos totales: {self.resultados_python.get('valores_nulos_totales', 'N/A')}\n")
            f.write(f"Registros únicos: {self.resultados_python.get('registros_unicos', 'N/A')}\n")
        
        print(f"✅ Script de Power BI generado: {script_filename}")
        return script_filename
    
    def generar_metricas_validacion(self):
        """
        Genera un archivo con métricas específicas para validar en Power BI
        """
        print("\n📋 GENERANDO MÉTRICAS DE VALIDACIÓN")
        print("=" * 50)
        
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
            f.write(f"Total de registros: {self.resultados_python.get('total_registros', 'N/A'):,}\n")
            f.write(f"Total de columnas: {self.resultados_python.get('total_columnas', 'N/A'):,}\n")
            f.write(f"Valores nulos totales: {self.resultados_python.get('valores_nulos_totales', 'N/A'):,}\n")
            f.write(f"Registros únicos: {self.resultados_python.get('registros_unicos', 'N/A'):,}\n")
            f.write(f"Memoria utilizada: {self.resultados_python.get('memoria_mb', 'N/A'):.2f} MB\n\n")
            
            # Distribución por género
            if 'distribucion_genero' in self.resultados_python:
                f.write("DISTRIBUCIÓN POR GÉNERO:\n")
                f.write("-" * 25 + "\n")
                for gender, count in self.resultados_python['distribucion_genero'].items():
                    percentage = (count / self.resultados_python['total_registros']) * 100
                    f.write(f"{gender}: {count:,} ({percentage:.1f}%)\n")
                f.write("\n")
            
            # Top 5 países
            if 'top_5_paises' in self.resultados_python:
                f.write("TOP 5 PAÍSES:\n")
                f.write("-" * 15 + "\n")
                for country, count in self.resultados_python['top_5_paises'].items():
                    percentage = (count / self.resultados_python['total_registros']) * 100
                    f.write(f"{country}: {count:,} ({percentage:.1f}%)\n")
                f.write("\n")
            
            # Top 5 lenguajes de programación
            if 'lenguajes_programacion' in self.resultados_python:
                f.write("TOP 5 LENGUAJES DE PROGRAMACIÓN:\n")
                f.write("-" * 35 + "\n")
                for i, (lang, count) in enumerate(list(self.resultados_python['lenguajes_programacion'].items())[:5], 1):
                    percentage = (count / self.resultados_python['total_registros']) * 100
                    f.write(f"{i}. {lang}: {count:,} ({percentage:.1f}%)\n")
                f.write("\n")
            
            # Top 3 plataformas de nube
            if 'plataformas_nube' in self.resultados_python:
                f.write("TOP 3 PLATAFORMAS DE NUBE:\n")
                f.write("-" * 30 + "\n")
                for i, (platform, count) in enumerate(list(self.resultados_python['plataformas_nube'].items())[:3], 1):
                    percentage = (count / self.resultados_python['total_registros']) * 100
                    f.write(f"{i}. {platform}: {count:,} ({percentage:.1f}%)\n")
                f.write("\n")
            
            f.write("FÓRMULAS DE POWER BI PARA VALIDACIÓN:\n")
            f.write("-" * 40 + "\n")
            f.write("Total de registros: = COUNTROWS(Tabla)\n")
            f.write("Total de columnas: = COLUMNS(Tabla)\n")
            f.write("Valores nulos: = SUMX(Tabla, IF(ISBLANK([Columna]), 1, 0))\n")
            f.write("Registros únicos: = DISTINCTCOUNT(Tabla[ID])\n")
            f.write("Distribución por género: = COUNTROWS(FILTER(Tabla, [Genero] = \"Male\"))\n")
        
        print(f"✅ Métricas de validación generadas: {filename}")
        return filename
    
    def crear_dashboard_powerbi(self):
        """
        Genera instrucciones para crear un dashboard en Power BI
        """
        print("\n📊 GENERANDO INSTRUCCIONES PARA DASHBOARD")
        print("=" * 50)
        
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
            f.write("   • Gráfico de barras horizontales: Lenguajes de programación\n")
            f.write("   • Gráfico de barras: Plataformas de nube\n")
            f.write("   • Gráfico de barras: Nivel educativo\n")
            f.write("   • Gráfico de barras: Áreas de estudio\n")
            f.write("   • Heatmap: Salario vs Experiencia\n")
            f.write("   • Gráfico de dispersión: Tiempo de encuesta vs Experiencia\n\n")
            
            f.write("3. MEDIDAS DAX RECOMENDADAS:\n")
            f.write("   • Total Encuestados = COUNTROWS(Tabla)\n")
            f.write("   • Porcentaje por Género = DIVIDE(COUNTROWS(FILTER(Tabla, [Genero] = \"Male\")), [Total Encuestados])\n")
            f.write("   • Promedio Tiempo Encuesta = AVERAGE(Tabla[Tiempo_Total_Encuesta_Segundos])\n")
            f.write("   • Top País = TOPN(1, VALUES(Tabla[Pais_Residencia]), COUNTROWS(Tabla))\n\n")
            
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
            f.write("   • Sección 3: Tecnologías (lenguajes, herramientas, nube)\n")
            f.write("   • Sección 4: Laboral (experiencia, salario, cargo)\n")
            f.write("   • Sección 5: Análisis cruzado (salario vs experiencia)\n\n")
            
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
        return filename
    
    def ejecutar_comparacion_completa(self):
        """
        Ejecuta la comparación completa entre Python y Power BI
        """
        print("🔄 EJECUTANDO COMPARACIÓN COMPLETA PYTHON vs POWER BI")
        print("=" * 60)
        
        # Calcular métricas en Python
        self.calcular_metricas_python()
        
        # Generar script de Power BI
        script_file = self.generar_script_powerbi()
        
        # Generar métricas de validación
        metrics_file = self.generar_metricas_validacion()
        
        # Generar instrucciones de dashboard
        dashboard_file = self.crear_dashboard_powerbi()
        
        print("\n✅ COMPARACIÓN COMPLETA FINALIZADA")
        print("📁 Archivos generados para validación en Power BI:")
        print(f"   • {script_file}")
        print(f"   • {metrics_file}")
        print(f"   • {dashboard_file}")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Abrir Power BI Desktop")
        print("2. Ejecutar el script de Power Query M")
        print("3. Comparar métricas con los valores esperados")
        print("4. Crear dashboard siguiendo las instrucciones")
        print("5. Validar que los resultados coincidan con Python")
        
        return {
            'script_file': script_file,
            'metrics_file': metrics_file,
            'dashboard_file': dashboard_file,
            'python_metrics': self.resultados_python
        }

def main():
    """
    Función principal para ejecutar la comparación
    """
    # Cargar el dataset limpio
    try:
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
        
        # Crear instancia del comparador
        comparador = ComparacionPowerBI(df_cleaned)
        
        # Ejecutar comparación completa
        resultados = comparador.ejecutar_comparacion_completa()
        
        print("\n🎉 ¡Comparación completada exitosamente!")
        print("📊 Los archivos están listos para validación en Power BI")
        
    except Exception as e:
        print(f"❌ Error al ejecutar la comparación: {str(e)}")

if __name__ == "__main__":
    main()

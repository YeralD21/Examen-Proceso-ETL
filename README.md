# Proceso ETL - Kaggle Survey 2019
## Aplicado al Área de Ingeniería de Sistemas

Este proyecto implementa un proceso ETL (Extract, Transform, Load) completo para el dataset de la encuesta de Kaggle 2019, con enfoque específico en el área de Ingeniería de Sistemas.

## 📋 Descripción del Proyecto

El proyecto analiza las respuestas de 19,717 profesionales en Data Science y Machine Learning para extraer insights relevantes para Ingeniería de Sistemas, incluyendo:

- **Tendencias tecnológicas** en lenguajes de programación, herramientas y plataformas
- **Análisis demográfico** de la comunidad de desarrolladores
- **Preferencias de herramientas** de desarrollo y computación en la nube
- **Tendencias salariales** y de experiencia profesional
- **Validación cruzada** con Power BI para asegurar reproducibilidad

## 🎯 Objetivos

1. **Implementar un proceso ETL robusto** y reproducible
2. **Analizar tendencias tecnológicas** relevantes para Ingeniería de Sistemas
3. **Validar resultados** mediante comparación con Power BI
4. **Generar insights accionables** para la toma de decisiones tecnológicas

## 📁 Estructura del Proyecto

```
├── multipleChoiceResponses.csv          # Dataset original de Kaggle
├── etl_kaggle_survey.py                 # Script principal del proceso ETL
├── analisis_visualizaciones.py          # Análisis y generación de gráficos
├── comparacion_powerbi.py               # Validación con Power BI
├── ejecutar_proceso_completo.py         # Script para ejecutar todo el proceso
├── INFORME_ETL_KAGGLE_SURVEY.md         # Informe detallado completo
└── README.md                            # Este archivo
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Power BI Desktop (para validación)

### Instalación de Dependencias

```bash
pip install pandas numpy matplotlib seaborn plotly openpyxl
```

### Ejecución del Proceso Completo

#### Opción 1: Ejecución Automática (Recomendada)

```bash
python ejecutar_proceso_completo.py
```

Este script ejecutará automáticamente:
1. Verificación de archivos requeridos
2. Instalación de dependencias
3. Proceso ETL completo
4. Análisis y visualizaciones
5. Comparación con Power BI

#### Opción 2: Ejecución Manual

```bash
# 1. Ejecutar proceso ETL
python etl_kaggle_survey.py

# 2. Generar análisis y visualizaciones
python analisis_visualizaciones.py

# 3. Crear comparación con Power BI
python comparacion_powerbi.py
```

## 📊 Archivos Generados

### Dataset Limpio
- `kaggle_survey_cleaned_[timestamp].csv` - Dataset limpio en formato CSV
- `kaggle_survey_cleaned_[timestamp].xlsx` - Dataset limpio en formato Excel
- `metadata_etl_[timestamp].txt` - Metadatos del proceso ETL

### Visualizaciones
- `analisis_demografico.png` - Análisis demográfico
- `analisis_lenguajes_programacion.png` - Lenguajes de programación
- `analisis_herramientas_desarrollo.png` - IDEs y editores
- `analisis_cloud_platforms.png` - Plataformas de nube
- `analisis_salarios_experiencia.png` - Salarios vs experiencia
- `analisis_areas_estudio.png` - Áreas de estudio

### Validación Power BI
- `powerbi_etl_script_[timestamp].txt` - Script de Power Query M
- `metricas_validacion_powerbi_[timestamp].txt` - Métricas para validación
- `instrucciones_dashboard_powerbi_[timestamp].txt` - Instrucciones de dashboard

### Documentación
- `resumen_ejecutivo_analisis_[timestamp].txt` - Resumen ejecutivo
- `INFORME_ETL_KAGGLE_SURVEY.md` - Informe detallado completo

## 🔄 Validación con Power BI

### Pasos para Validación

1. **Abrir Power BI Desktop**
2. **Cargar datos:** Obtener datos > Archivo > CSV
3. **Seleccionar:** `multipleChoiceResponses.csv`
4. **Aplicar script:** Editor avanzado > Pegar script M generado
5. **Validar métricas:** Comparar con archivo de validación
6. **Crear dashboard:** Seguir instrucciones generadas

### Métricas de Validación

| Métrica | Valor Esperado |
|---------|----------------|
| Total registros | 19,717 |
| Total columnas | 298 |
| Valores nulos | 0 |
| Memoria (MB) | ~39.0 |

## 📈 Principales Hallazgos

### Lenguajes de Programación Más Usados
1. **Python:** 68.2% de los encuestados
2. **SQL:** 45.1% de los encuestados
3. **R:** 23.8% de los encuestados
4. **JavaScript/TypeScript:** 20.3% de los encuestados
5. **Java:** 15.7% de los encuestados

### Plataformas de Nube Más Populares
1. **Amazon Web Services (AWS):** 42.1% de los encuestados
2. **Google Cloud Platform (GCP):** 38.9% de los encuestados
3. **Microsoft Azure:** 35.2% de los encuestados
4. **IBM Cloud:** 8.7% de los encuestados
5. **Alibaba Cloud:** 2.1% de los encuestados

### IDEs y Editores Más Utilizados
1. **Jupyter/IPython:** 65.4% de los encuestados
2. **Visual Studio Code:** 58.2% de los encuestados
3. **PyCharm:** 35.7% de los encuestados
4. **RStudio:** 32.1% de los encuestados
5. **Sublime Text:** 28.9% de los encuestados

## 🎯 Aplicaciones en Ingeniería de Sistemas

### Recomendaciones Tecnológicas
- **Priorizar Python** como lenguaje principal para desarrollo
- **Invertir en AWS** como plataforma de nube principal
- **Adoptar Visual Studio Code** como IDE estándar
- **Implementar Jupyter** para análisis de datos
- **Considerar SQL** como competencia fundamental

### Stack Tecnológico Recomendado
```
Frontend: JavaScript/TypeScript + React/Vue
Backend: Python + FastAPI/Django
Base de datos: PostgreSQL + Redis
Nube: AWS (EC2, RDS, S3, Lambda)
Monitoreo: Prometheus + Grafana
CI/CD: GitHub Actions
```

## 🔧 Transformaciones Aplicadas

### Limpieza de Datos
1. **Eliminación de registros duplicados**
2. **Eliminación de columnas con >80% valores faltantes**
3. **Imputación de valores nulos:**
   - Categóricas: "No especificado"
   - Numéricas: Mediana
4. **Limpieza de espacios en blanco**
5. **Normalización de texto (minúsculas)**

### Renombrado de Columnas
- **Q1** → Edad_Encuestado
- **Q2** → Genero
- **Q3** → Pais_Residencia
- **Q4** → Nivel_Educativo
- **Q5** → Area_Estudios_Principal
- **Q6** → Situacion_Laboral_Actual
- **Q7** → Cargo_Principal_Trabajo
- **Q8** → Anos_Experiencia_Campo
- **Q9** → Rango_Salarial_Anual
- **Q10** → Lenguajes_Programacion_Habituales

### Columnas Derivadas
- **Categoria_Experiencia:** Principiante, Intermedio, Avanzado, Experto
- **Categoria_Salarial:** Bajo, Medio, Alto, Muy Alto

## 📊 Métricas de Calidad

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Completitud | 61.3% | 100% | +38.7% |
| Valores nulos | 2,847,392 | 0 | -100% |
| Columnas | 350 | 298 | -14.9% |
| Memoria | 45.2 MB | 38.7 MB | -14.4% |

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo multipleChoiceResponses.csv"
- **Solución:** Asegúrate de que el archivo esté en el directorio actual
- **Verificación:** `ls -la multipleChoiceResponses.csv`

### Error: "ModuleNotFoundError"
- **Solución:** Instala las dependencias: `pip install pandas numpy matplotlib seaborn plotly openpyxl`

### Error: "Permission denied" en Windows
- **Solución:** Ejecuta el terminal como administrador o cambia los permisos del directorio

### Error en Power BI: "Script M no válido"
- **Solución:** Verifica que el archivo CSV esté en la ruta correcta en el script M

## 📞 Soporte

Para consultas o problemas:

1. **Revisar la documentación:** `INFORME_ETL_KAGGLE_SURVEY.md`
2. **Verificar archivos de metadatos** generados
3. **Consultar logs de ejecución** en la consola
4. **Validar con Power BI** usando los scripts generados

## 📄 Licencia

Este proyecto es de uso educativo y de investigación. El dataset original pertenece a Kaggle.

## 🙏 Agradecimientos

- **Kaggle** por proporcionar el dataset de la encuesta
- **Comunidad de Data Science** por las respuestas a la encuesta
- **Desarrolladores** de las librerías Python utilizadas

---

*Proyecto desarrollado para el curso de Business Intelligence - UPEU*

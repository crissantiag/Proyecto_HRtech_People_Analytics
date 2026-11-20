# HRTech People Analytics

Proyecto integrador **«De la ingesta al valor estratégico»** de la asignatura *Gestión de Datos para Inteligencia Artificial y Big Data* (COIDS1604), ITCA-FEPADE, Ingeniería en Desarrollo de Software.

El proyecto recorre el ciclo completo de un caso de analítica de Recursos Humanos: integración de fuentes heterogéneas, limpieza e ingeniería de características, arquitectura Big Data, gobernanza y ética, visualización (Power BI), análisis geoespacial (ArcGIS), reportería profesional y modelos predictivos de Machine Learning con optimización de hiperparámetros.

**Integrantes:** Aleyda Lisseth Cruz Paz · María Elizabeth Diaz Lara · Cristina Nohemy Fuentes Santiago · Helen Margarita Martínez Clímaco · Liliana Elizabeth Munguia Quezada · Josué Estiven Valdes Mendoza
**Docente:** Ing. Gilbert García

> Todos los datos son **ficticios** y de uso académico.

---

## Estructura de la carpeta

```
Proyecto_HRtech_People_Analytics/
├── README.md
├── Proyecto_HRtech_People_Analytics_.ipynb   # Notebook integrador (Guías 1 a 10)
├── Documento Final HRTech People Analytics.pdf
│
├── notebooks/                # Un notebook por guía (01 a 10)
├── scripts/                  # Scripts reproducibles de las Guías 1 y 2 + modelo entrenado
├── sql/                      # Estructura y datos de la tabla de capacitaciones
├── datos/                    # Datos por etapa (crudos → procesados → gobernanza)
├── geo/                      # Datos geoespaciales validados (Guía 6)
├── visualizaciones/          # Dashboard de Power BI (.pbix)
├── template/                 # Plantilla HTML del informe gerencial
├── documentos/               # Diccionario, matrices, bitácoras, política, informe
├── evidencias/               # Avances, dashboards, mapas, informe y entregables del modelo
├── capturas/                 # Capturas de pantalla del desarrollo (guia1 a guia10)
└── presentacion/             # Presentación de la defensa final (PDF)
```

---

## Guías del proyecto

| Guía | Tema | Notebook | Resultado principal |
|---|---|---|---|
| 1 | Fuentes heterogéneas | `guia_01_fuentes_heterogeneas.ipynb` | Integración de CSV + SQL + JSON en un dataset único |
| 2 | Limpieza e ingeniería de características | `guia_02_limpieza_ingenieria_caracteristicas.ipynb` | Dataset limpio con variables derivadas |
| 3 | Arquitectura Big Data | `guia_03_arquitectura_bigdata.ipynb` | Procesamiento con PySpark y formato Parquet |
| 4 | Gobernanza y ética | `guia_04_gobernanza_etica.ipynb` | Política de gobernanza, matriz de riesgos y dataset publicable anonimizado |
| 5 | Visualización con Power BI | `guia_05_visualizacion_powerbi.ipynb` | Dashboard `.pbix` y validación de KPIs contra la fuente |
| 6 | Análisis geoespacial con ArcGIS | `guia_06_analisis_geoespacial_arcgis.ipynb` | Mapas de cobertura, sucursales y demanda |
| 7 | Reportería profesional | `guia_07_reporteria_profesional.ipynb` | Informe gerencial en DOCX y PDF con gráficos |
| 8 | Fundamentos de predicción con IA | `guia_08_fundamentos_prediccion_ia.ipynb` | Definición de variable objetivo y dataset de modelado |
| 9 | Enfrentamiento de modelos de ML | `guia_09_enfrentamiento_modelos_ml.ipynb` | Comparación de modelos y modelo candidato |
| 10 | Optimización de hiperparámetros | `guia_10_optimizacion_hiperparametros.ipynb` | `GridSearchCV` y comparación final contra la Guía 9 |

Los notebooks están pensados para ejecutarse en **Google Colab** (usan rutas `/content/` y, en la Guía 10, montaje de Google Drive).

---

## Fuentes de datos

| Fuente | Tipo | Ubicación | Contenido |
|---|---|---|---|
| Empleados | CSV | `datos/crudos/empleados.csv` | Datos generales, desempeño, salario y estado |
| Capacitaciones | SQLite | `datos/crudos/empresa_hr_analytics.db` | Cursos, horas y resultado |
| Datos adicionales | JSON | `datos/externos/datos_adicionales.json` | Satisfacción y horas extra |

Las tres se cruzan por `id_empleado` (10 empleados). La tabla `capacitaciones` se define en `sql/estructura_inicial.sql`.

### Carpeta `datos/`

| Subcarpeta | Archivos | Descripción |
|---|---|---|
| `crudos/` | `empleados.csv`, `empresa_hr_analytics.db` | Datos originales, sin modificar |
| `externos/` | `datos_adicionales.json` | Fuente externa en JSON |
| `procesados/` | `dataset_integrado_…csv`, `dataset_con_errores_…csv`, `dataset_limpio_…csv` | Salida de las Guías 1 y 2 (el dataset con errores es el ejercicio de limpieza) |
| | `indicadores_iniciales.csv` | % de inactivos (30 %), desempeño promedio (81.9), satisfacción promedio (3.7) |
| | `predicciones_hrtech_people_analytics.csv`, `predicciones_guia09_hrtech.csv` | Predicciones de los modelos |
| `gobernanza/` | `dataset_publicable_HRTech_People_Analytics.csv` | Vista analítica protegida: identificadores tokenizados y valores exactos reemplazados por rangos |
| `analiticos/` | *(vacía)* | Reservada para datasets analíticos |

---

## Scripts

Reconstrucción ejecutable de las Guías 1 y 2 (el resto del trabajo vive en los notebooks).

| Archivo | Qué hace |
|---|---|
| `scripts/conexion_fuentes.py` | Crea las fuentes, integra CSV + SQL + JSON, valida cardinalidad y genera `indicadores_iniciales.csv` |
| `scripts/limpieza_datos.py` | Normaliza textos y columnas, trata nulos, duplicados y salarios negativos, y crea variables derivadas (`salario_por_hora`, `categoria_antiguedad`, `rango_edad`, `requiere_capacitacion`, etc.) |
| `scripts/modelo_candidato_guia09_hrtech.joblib` | Modelo entrenado en la Guía 9 |

### Requisitos

- Python 3.9+
- `pandas`, `numpy`, `openpyxl` (opcional, para el reporte de calidad en Excel)
- Para los notebooks: `pyspark` (Guía 3), `jinja2`, `weasyprint`, `python-docx` (Guía 7), `scikit-learn` (Guías 8 a 10)

```bash
pip install pandas numpy openpyxl
```

### Ejecución

Desde la raíz del proyecto, en este orden:

```bash
python scripts/conexion_fuentes.py
python scripts/limpieza_datos.py
```

Opciones:

- `--base RUTA`: carpeta donde se crean `datos/` y `documentos/` (por defecto, la actual).
- `--simular-errores` (solo `limpieza_datos.py`): inyecta errores controlados (espacios, mayúsculas, un nulo, un salario negativo y un duplicado) para practicar la limpieza.

Para crear solo la base de datos:

```bash
sqlite3 datos/crudos/empresa_hr_analytics.db < sql/estructura_inicial.sql
```

---

## Gobernanza y ética (Guía 4)

La política completa está en `documentos/politica_gobernanza_HRTech_People_Analytics.md`. Define:

- **Clasificación de datos:** Público, Interno, Confidencial y Restringido.
- **Acceso por rol:** Administrador de RRHH, Analista de People Analytics (solo la vista protegida), Auditor / Comité de ética y Empleado titular.
- **Minimización, retención y ética:** sin decisiones automatizadas de contratación, despido o ascenso; resultados siempre agregados.

Se complementa con `matriz_riesgos_HRTech_People_Analytics.xlsx` (8 riesgos con probabilidad, impacto, control y nivel).

---

## Modelo predictivo (Guías 8 a 10)

- **Variable objetivo:** `requiere_capacitacion`.
- **Datos:** 600 registros sintéticos (480 entrenamiento / 120 prueba), 12 variables, `random_state = 42`.
- **Optimización:** `GridSearchCV` sobre `RandomForestClassifier`, validación `StratifiedKFold(4)`, métrica `recall`.

| Modelo | Accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|
| Baseline | 0.575 | 0.000 | 0.000 | 0.000 | 0.500 |
| Guía 9 (sin optimizar) | 0.708 | 0.667 | 0.627 | 0.646 | 0.743 |
| Guía 10 (optimizado) | 0.683 | 0.623 | 0.647 | 0.635 | 0.758 |

La optimización mejora levemente el **recall** y el **ROC AUC**, a costa de algo de accuracy y precisión. El detalle está en `evidencias/entregables_guia10_hrtech.zip` (modelo `.joblib`, resultados del grid, top 10 de errores, predicciones y metadatos).

---

## Documentación (`documentos/`)

| Archivo | Contenido |
|---|---|
| `Diccionario_de_datos_4.4.xlsx` | Diccionario de datos del dataset |
| `inventario_fuentes/` | Copia de las fuentes e `inventario_fuentes.xlsx` |
| `matriz_riesgos_HRTech_People_Analytics.xlsx` | Matriz de riesgos de gobernanza |
| `matriz_recomendaciones_HRTech.xlsx` | Hallazgos, acciones, prioridad, responsable y KPI de seguimiento |
| `matriz_trazabilidad_HRTech.xlsx` | Trazabilidad hallazgo → recomendación, KPI → fuente y archivos generados |
| `valores_fuente_guia05_HRTech.csv` | KPIs de referencia para validar el dashboard (10 colaboradores, desempeño 81.9, inactividad 30 %, antigüedad 4.6 años, 90 h de capacitación) |
| `politica_gobernanza_HRTech_People_Analytics.md` | Política de gobernanza de datos |
| `informe_hrtech.pdf` | Informe gerencial |
| `bitacora_semans_01_04.docx`, `_05_08.docx`, `_09_10.docx` | Bitácoras de trabajo por semanas |

## Evidencias (`evidencias/`)

- `Avance1_…docx` y `Avance2_…docx`: documentos de los avances 1 y 2.
- `guia05_dashboard/`: capturas del resumen ejecutivo y detalle del dashboard.
- `guia06_mapa/`: capturas de los mapas de ArcGIS y `link del mapa.txt` con el enlace al mapa web.
- `guia07_informe/`: informe en DOCX/PDF y gráficos (canal, categorías, región, tendencia).
- `empleados_analiticos_parquet.zip`: dataset analítico en formato Parquet (Guía 3).
- `entregables_guia10_hrtech.zip`: entregables de la optimización del modelo.

## Otros recursos

- `visualizaciones/guia05_avance2_HRTech_People_Analytics.pbix`: dashboard de Power BI.
- `geo/`: `demanda_hrtech_guia06_validado.csv` y `sucursales_hrtech_guia06_validado.csv`.
- `template/plantilla_hrtech.html`: plantilla del informe gerencial (Jinja2).
- `presentacion/Presentación Defensa Final.pdf`: presentación de la defensa final.
- `capturas/guia1` … `guia10`: capturas paso a paso de cada guía.

---

## Notas

- Los datos reales de empleados (nombre, salario, desempeño) son ficticios; aun así, el proyecto aplica la política de gobernanza y comparte únicamente la vista protegida de `datos/gobernanza/`.
- Los resultados del modelo se basan en datos sintéticos, por lo que sirven como ejercicio metodológico y no como evidencia de negocio.

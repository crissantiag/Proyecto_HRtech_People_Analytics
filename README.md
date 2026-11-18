# HRTech People Analytics

Pipeline inicial del proyecto: integra tres fuentes de datos de RRHH (CSV, SQL y JSON) y deja un dataset limpio listo para análisis.

## Estructura

```
proyecto_hrtech/
├── sql/
│   └── estructura_inicial.sql      # Tabla capacitaciones + datos (SQLite)
├── scripts/
│   ├── conexion_fuentes.py         # Guía 1: integración de fuentes
│   └── limpieza_datos.py           # Guía 2: limpieza y variables derivadas
├── datos/                          # Se crea al ejecutar
│   ├── crudos/                     # empleados.csv, empresa_hr_analytics.db
│   ├── externos/                   # datos_adicionales.json
│   └── procesados/                 # datasets integrado y limpio, indicadores
└── documentos/                     # reporte de calidad
```

## Fuentes de datos

| Fuente | Tipo | Ubicación | Contenido |
|---|---|---|---|
| Empleados | CSV | `datos/crudos/empleados.csv` | Datos generales y desempeño |
| Capacitaciones | SQL (SQLite) | `datos/crudos/empresa_hr_analytics.db` | Cursos, horas y resultado |
| Datos adicionales | JSON | `datos/externos/datos_adicionales.json` | Satisfacción y horas extra |

Las tres se cruzan por `id_empleado` (left join, 10 empleados).

## Requisitos

- Python 3.9+
- `pandas` y `numpy`
- `openpyxl` (opcional, para el reporte en Excel; si falta se guarda como CSV)

```bash
pip install pandas numpy openpyxl
```

## Ejecución

Desde la carpeta raíz del proyecto, en este orden:

```bash
python scripts/conexion_fuentes.py
python scripts/limpieza_datos.py
```

Opciones:

- `--base RUTA`: carpeta donde se crean `datos/` y `documentos/` (por defecto, la carpeta actual).
- `--simular-errores` (solo `limpieza_datos.py`): inyecta los errores controlados de la guía (espacios y mayúsculas en departamento, un nulo, un salario negativo y un duplicado) para practicar la limpieza.

Para crear solo la base de datos:

```bash
sqlite3 datos/crudos/empresa_hr_analytics.db < sql/estructura_inicial.sql
```

## Qué hace cada script

**`conexion_fuentes.py`**
1. Crea las carpetas y las tres fuentes.
2. Integra CSV + SQL + JSON y calcula `salario_anual` y `horas_capacitacion`.
3. Valida cardinalidad (filas, columnas, duplicados, nulos).
4. Genera `indicadores_iniciales.csv`: % de inactivos, desempeño promedio y satisfacción promedio.

**`limpieza_datos.py`**
1. Normaliza nombres de columnas, espacios y categorías (`IT`, `RRHH`, etc.).
2. Completa nulos (`Sin curso asignado`, `Sin evaluar`) y elimina duplicados.
3. Convierte tipos y corrige salarios negativos.
4. Recalcula `salario_anual` y `salario_por_hora`.
5. Crea `categoria_antiguedad` (Junior/Senior), `rango_edad`, `es_antiguo` y `requiere_capacitacion`.
6. Guarda el reporte de calidad y `dataset_limpio_HRTech_People_Analytics.csv` (22 columnas).

## Salidas

- `datos/procesados/dataset_integrado_HRTech_People_Analytics.csv`
- `datos/procesados/indicadores_iniciales.csv`
- `datos/procesados/dataset_limpio_HRTech_People_Analytics.csv`
- `documentos/reporte_calidad_HRTech_People_Analytics.xlsx`

## Notas

- Los datos son ficticios y de ejemplo.
- Los scripts son una reconstrucción basada en las Guías 1 y 2 del notebook `Proyecto_HRtech_People_Analytics_.ipynb`.
- Las Guías 3 en adelante (Spark, gobernanza, visualización, informes) siguen en el notebook.

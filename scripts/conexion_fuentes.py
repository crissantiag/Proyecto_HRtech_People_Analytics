"""
conexion_fuentes.py  |  HRTech People Analytics (Guía 1)

Conecta e integra las tres fuentes del proyecto:
  1. CSV   -> datos/crudos/empleados.csv
  2. SQL   -> datos/crudos/empresa_hr_analytics.db (tabla capacitaciones)
  3. JSON  -> datos/externos/datos_adicionales.json
y genera datos/procesados/dataset_integrado_HRTech_People_Analytics.csv

Uso:  python scripts/conexion_fuentes.py [--base RUTA]
"""
import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "estructura_inicial.sql"


def definir_rutas(base: Path) -> dict:
    rutas = {
        "raw": base / "datos" / "crudos",
        "processed": base / "datos" / "procesados",
        "external": base / "datos" / "externos",
    }
    for r in rutas.values():
        r.mkdir(parents=True, exist_ok=True)
    return rutas


def crear_empleados_csv(ruta_csv: Path) -> None:
    """Datos de empleados (fuente 1: CSV)."""
    empleados = pd.DataFrame({
        "id_empleado": range(1, 11),
        "nombre": ["Ana", "Luis", "Carlos", "María", "Sofía",
                   "José", "Laura", "Daniel", "Paola", "Miguel"],
        "departamento": ["Ventas", "IT", "Finanzas", "RRHH", "Marketing",
                         "IT", "Ventas", "Finanzas", "RRHH", "Marketing"],
        "edad": [25, 31, 28, 35, 29, 26, 40, 33, 27, 38],
        "desempeño": [85, 92, 70, 88, 78, 95, 65, 82, 90, 74],
        "salario": [550, 900, 650, 750, 700, 950, 600, 800, 720, 680],
        "tiempo_empresa_anios": [2, 5, 1, 7, 3, 2, 10, 6, 2, 8],
        "estado_empleado": ["Activo", "Activo", "Inactivo", "Activo", "Activo",
                            "Activo", "Inactivo", "Activo", "Activo", "Inactivo"],
    })
    empleados.to_csv(ruta_csv, index=False, encoding="utf-8")


def crear_base_sql(ruta_db: Path, sql_file: Path = SQL_FILE) -> None:
    """Fuente 2: crea/actualiza la BD SQLite ejecutando estructura_inicial.sql."""
    with sqlite3.connect(ruta_db) as con:
        con.executescript(sql_file.read_text(encoding="utf-8"))


def crear_json(ruta_json: Path) -> None:
    """Fuente 3: datos adicionales (satisfacción y horas extra)."""
    satisfaccion = [4, 5, 2, 4, 3, 5, 2, 4, 5, 3]
    horas_extra = [5, 3, 12, 4, 8, 2, 14, 5, 3, 9]
    datos = [{"id_empleado": i + 1, "satisfaccion": s, "horas_extra": h}
             for i, (s, h) in enumerate(zip(satisfaccion, horas_extra))]
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def integrar(ruta_csv: Path, ruta_db: Path, ruta_json: Path) -> pd.DataFrame:
    df_emp = pd.read_csv(ruta_csv)
    df_emp["salario_anual"] = df_emp["salario"] * 12

    with sqlite3.connect(ruta_db) as con:
        df_cap = pd.read_sql_query("SELECT * FROM capacitaciones;", con)

    df_json = pd.read_json(ruta_json)

    df_int = pd.merge(df_emp, df_cap, on="id_empleado", how="left")
    df_int["horas_capacitacion"] = df_int["horas"]
    df_final = pd.merge(df_int, df_json, on="id_empleado", how="left")

    print("VALIDACIÓN DE CARDINALIDAD")
    print(f"Filas: {len(df_int)} -> {len(df_final)}")
    print(f"Columnas: {len(df_int.columns)} -> {len(df_final.columns)}")
    print(f"Duplicados: {df_int.duplicated().sum()} -> {df_final.duplicated().sum()}")
    print("Nulos por columna:\n", df_final.isnull().sum())
    assert len(df_final) == len(df_emp), "El join cambió el número de filas"
    return df_final


def indicadores_iniciales(df: pd.DataFrame) -> pd.DataFrame:
    pct_inactivos = (df["estado_empleado"] == "Inactivo").mean() * 100
    return pd.DataFrame({
        "indicador": ["Porcentaje de empleados inactivos (%)",
                      "Promedio de desempeño", "Promedio de satisfacción"],
        "valor": [pct_inactivos, df["desempeño"].mean(), df["satisfaccion"].mean()],
    })


def inventario_fuentes() -> pd.DataFrame:
    return pd.DataFrame({
        "fuente": ["Empleados", "Capacitaciones", "Datos adicionales"],
        "tipo": ["CSV", "SQL", "JSON"],
        "ubicacion": ["datos/crudos/empleados.csv",
                      "datos/crudos/empresa_hr_analytics.db",
                      "datos/externos/datos_adicionales.json"],
        "descripcion": ["Datos generales y desempeño de empleados",
                        "Información de cursos y horas de capacitación",
                        "Satisfacción y horas extra"],
    })


def main(base: Path) -> pd.DataFrame:
    r = definir_rutas(base)
    ruta_csv = r["raw"] / "empleados.csv"
    ruta_db = r["raw"] / "empresa_hr_analytics.db"
    ruta_json = r["external"] / "datos_adicionales.json"

    crear_empleados_csv(ruta_csv)
    crear_base_sql(ruta_db)
    crear_json(ruta_json)

    df_final = integrar(ruta_csv, ruta_db, ruta_json)
    df_final.to_csv(r["processed"] / "dataset_integrado_HRTech_People_Analytics.csv",
                    index=False)
    indicadores = indicadores_iniciales(df_final)
    indicadores.to_csv(r["processed"] / "indicadores_iniciales.csv", index=False)

    print("\nInventario de fuentes:\n", inventario_fuentes())
    print("\nIndicadores:\n", indicadores)
    return df_final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".", help="Carpeta base del proyecto")
    main(Path(ap.parse_args().base))

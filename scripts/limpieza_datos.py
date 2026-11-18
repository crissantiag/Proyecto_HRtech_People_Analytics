"""
limpieza_datos.py  |  HRTech People Analytics (Guía 2)

Limpia el dataset integrado de la Guía 1:
  - normaliza nombres de columnas y textos (strip / title / IT / RRHH)
  - completa nulos, elimina duplicados, convierte tipos
  - corrige salarios negativos y recalcula variables derivadas
  - crea variables de antigüedad, rango de edad y requiere_capacitacion
  - genera reporte de calidad (.xlsx) y dataset limpio (.csv)

Uso:  python scripts/limpieza_datos.py [--base RUTA] [--simular-errores]
  --simular-errores  inyecta los errores controlados de la guía
                     (espacios/mayúsculas, nulo, salario negativo, duplicado)
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

MAPEO_DEPTOS = {"ventas": "Ventas", "it": "IT", "finanzas": "Finanzas",
                "rrhh": "RRHH", "marketing": "Marketing"}


def simular_errores(df: pd.DataFrame) -> pd.DataFrame:
    e = df.copy()
    e.loc[0, "departamento"] = " ventas "
    e.loc[1, "departamento"] = "it"
    e.loc[4, "departamento"] = "MARKETING "
    e.loc[3, "resultado"] = np.nan
    e.loc[2, "salario"] = -650
    return pd.concat([e, e.iloc[[0]]], ignore_index=True)


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

    # Textos: strip + normalización de categorías
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()
    df["departamento"] = df["departamento"].str.lower().map(MAPEO_DEPTOS).fillna(df["departamento"])
    for col in ["curso", "resultado", "estado_empleado"]:
        if col in df.columns:
            df[col] = df[col].str.title()

    # Nulos y duplicados
    df["curso"] = df["curso"].fillna("Sin curso asignado")
    df["resultado"] = df["resultado"].fillna("Sin evaluar")
    df = df.drop_duplicates().reset_index(drop=True)

    # Tipos numéricos
    for col in ["edad", "desempeño", "tiempo_empresa_anios", "horas",
                "satisfaccion", "horas_extra"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["salario", "salario_anual"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

    # Salarios negativos y variables derivadas
    df["salario"] = df["salario"].abs()
    df["salario_anual"] = df["salario"] * 12
    df["salario_por_hora"] = df["salario"] / df["horas"]

    # Características temporales / demográficas
    df["anios_redondeados"] = df["tiempo_empresa_anios"].round()
    df["es_antiguo"] = df["tiempo_empresa_anios"] >= 5
    df["categoria_antiguedad"] = np.where(df["tiempo_empresa_anios"] >= 5, "Senior", "Junior")
    df["rango_edad"] = np.select(
        [df["edad"] < 30, df["edad"] <= 50],
        ["Joven (<30)", "Adulto (30-50)"], default="Mayor (>50)")
    df["requiere_capacitacion"] = df["resultado"] == "Reprobado"
    return df


def reporte_calidad(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "columna": df.columns,
        "tipo_dato": [str(df[c].dtype) for c in df.columns],
        "valores_nulos": [df[c].isnull().sum() for c in df.columns],
        "valores_unicos": [df[c].nunique() for c in df.columns],
    })


def main(base: Path, con_errores: bool = False) -> pd.DataFrame:
    procesados = base / "datos" / "procesados"
    documentos = base / "documentos"
    procesados.mkdir(parents=True, exist_ok=True)
    documentos.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(procesados / "dataset_integrado_HRTech_People_Analytics.csv")
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

    if con_errores:
        df = simular_errores(df)
        df.to_csv(procesados / "dataset_con_errores_HRTech_People_Analytics.csv",
                  index=False, encoding="utf-8")
        print(f"Errores simulados: {df.shape[0]} filas")

    df_limpio = limpiar(df)
    reporte = reporte_calidad(df_limpio)
    try:
        reporte.to_excel(documentos / "reporte_calidad_HRTech_People_Analytics.xlsx", index=False)
    except ImportError:
        reporte.to_csv(documentos / "reporte_calidad_HRTech_People_Analytics.csv", index=False)
        print("openpyxl no disponible: reporte guardado como CSV")

    df_limpio.to_csv(procesados / "dataset_limpio_HRTech_People_Analytics.csv",
                     index=False, encoding="utf-8")
    print(f"Dataset limpio: {df_limpio.shape[0]} filas, {df_limpio.shape[1]} columnas")
    return df_limpio


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=".", help="Carpeta base del proyecto")
    ap.add_argument("--simular-errores", action="store_true")
    a = ap.parse_args()
    main(Path(a.base), a.simular_errores)

"""
Script: graficar_boxplot.py
Descripción: Genera gráficos tipo boxplot para visualizar la presencia de outliers en datos de ventas,
             antes y después del proceso de limpieza con IQR.
Autor: Jorge Alexander Valencia
Fecha: 2025
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


def cargar_datos(ruta_csv):
    """Carga un archivo CSV y devuelve un DataFrame de pandas."""
    try:
        df = pd.read_csv(ruta_csv)
        print(f"✅ Datos cargados correctamente desde {ruta_csv}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: el archivo {ruta_csv} no fue encontrado.")
        return None


def graficar_boxplot(df, columna, titulo, nombre_archivo):
    """
    Genera un gráfico boxplot de una columna específica.

    Parámetros:
    - df: DataFrame de pandas con los datos
    - columna: nombre de la columna numérica a graficar (ej: 'ventas')
    - titulo: título que aparecerá en el gráfico
    - nombre_archivo: nombre del archivo .png a guardar
    """
    if df is None or columna not in df.columns:
        print(f"⚠️ Datos inválidos o columna '{columna}' no encontrada.")
        return

    plt.figure(figsize=(8, 4))
    sns.boxplot(x=df[columna], color="#2E86C1")
    plt.title(titulo)
    plt.xlabel(columna)
    plt.tight_layout()

    plt.savefig(nombre_archivo)
    plt.close()
    print(f"📈 Gráfico guardado como {nombre_archivo}")


if __name__ == "__main__":
    # Rutas relativas
    ruta_original = os.path.join("ventas.csv")
    ruta_limpia = os.path.join("ventas_limpias.csv")

    # Cargar datos
    datos_originales = cargar_datos(ruta_original)
    datos_limpios = cargar_datos(ruta_limpia)

    # Generar gráficos
    graficar_boxplot(
        datos_originales,
        columna="ventas",
        titulo="Distribución de Ventas (Antes de limpieza)",
        nombre_archivo="assets/images/boxplot_antes.png"
    )

    graficar_boxplot(
        datos_limpios,
        columna="ventas",
        titulo="Distribución de Ventas (Después de limpieza)",
        nombre_archivo="assets/images/boxplot_despues.png"
    )

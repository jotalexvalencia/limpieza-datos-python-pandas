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
import sys

# === 🎯 Configuración de rutas ===
ORIGINAL_CSV = "ventas.csv"
LIMPIO_CSV = "ventas_limpias.csv"
IMG_DIR = "assets/images"
IMG_ANTES = os.path.join(IMG_DIR, "boxplot_antes.png")
IMG_DESPUES = os.path.join(IMG_DIR, "boxplot_despues.png")


def cargar_datos(ruta_csv):
    """Carga un archivo CSV y devuelve un DataFrame de pandas."""
    if not os.path.exists(ruta_csv):
        print(f"❌ Error: el archivo {ruta_csv} no fue encontrado.")
        return None
    try:
        df = pd.read_csv(ruta_csv)
        print(f"✅ Datos cargados correctamente desde {ruta_csv}")
        return df
    except Exception as e:
        print(f"❌ Error al leer {ruta_csv}: {str(e)}")
        return None


def graficar_boxplot(df, columna, titulo, ruta_salida):
    """
    Genera un gráfico boxplot de una columna específica y lo guarda como imagen.

    Parámetros:
    - df: DataFrame de pandas con los datos
    - columna: nombre de la columna numérica a graficar (ej: 'ventas')
    - titulo: título que aparecerá en el gráfico
    - ruta_salida: ruta completa del archivo .png a guardar
    """
    if df is None or columna not in df.columns:
        print(f"⚠️ Datos inválidos o columna '{columna}' no encontrada.")
        return

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    plt.figure(figsize=(8, 4))
    sns.boxplot(x=df[columna], color="#2E86C1")
    plt.title(titulo)
    plt.xlabel(columna)
    plt.tight_layout()

    try:
        plt.savefig(ruta_salida)
        print(f"📈 Gráfico guardado como {ruta_salida}")
    except Exception as e:
        print(f"❌ Error al guardar gráfico: {str(e)}")
    finally:
        plt.close()


def main():
    # Cargar datos
    df_original = cargar_datos(ORIGINAL_CSV)
    df_limpio = cargar_datos(LIMPIO_CSV)

    # Generar gráficos
    graficar_boxplot(
        df_original,
        columna="ventas",
        titulo="Distribución de Ventas (Antes de limpieza)",
        ruta_salida=IMG_ANTES
    )

    graficar_boxplot(
        df_limpio,
        columna="ventas",
        titulo="Distribución de Ventas (Después de limpieza)",
        ruta_salida=IMG_DESPUES
    )


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        sys.exit(1)

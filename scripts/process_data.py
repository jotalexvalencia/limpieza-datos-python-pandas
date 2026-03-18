# === scripts/process_data.py ===
import pandas as pd
import os
import sys

# === 🧠 Función Pura (Lógica de Negocio) ===
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the sales DataFrame by removing nulls and outliers.
    
    Args:
        df (pd.DataFrame): Raw input data with 'ventas' column.
        
    Returns:
        pd.DataFrame: Cleaned data without outliers.
        
    Raises:
        ValueError: If columns are missing.
    """
    # Validate structure
    esperadas = ['fecha', 'producto', 'ventas', 'region']
    if list(df.columns) != esperadas:
        raise ValueError(f"Invalid columns. Expected: {esperadas}")

    # Type conversion
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce')

    # Drop nulls
    df.dropna(inplace=True)

    # IQR Outlier Detection
    Q1 = df['ventas'].quantile(0.25)
    Q3 = df['ventas'].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR

    df = df[(df['ventas'] >= lim_inf) & (df['ventas'] <= lim_sup)]
    return df

# === 🚀 Ejecución Principal (Script) ===
if __name__ == "__main__":
    ENTRADA = "ventas.csv"
    SALIDA = "ventas_limpias.csv"
    
    try:
        if not os.path.exists(ENTRADA):
            raise FileNotFoundError(f"❌ El archivo '{ENTRADA}' no fue encontrado.")

        df = pd.read_csv(ENTRADA)
        df_limpio = limpiar_datos(df) # Llamamos a la función pura
        
        df_limpio.to_csv(SALIDA, index=False)
        
        print(f"✅ Limpieza completada: {SALIDA}")
        print(f"🧾 Registros eliminados: {len(df) - len(df_limpio)}")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error en limpieza de datos: {str(e)}")
        sys.exit(1)
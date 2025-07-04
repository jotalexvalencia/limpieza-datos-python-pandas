# === scripts/process_data.py ===
# Limpieza de datos de ventas (eliminación de outliers y validación de estructura)

import pandas as pd
import os
import sys

# === 📍 Rutas de entrada/salida ===
ENTRADA = "ventas.csv"
SALIDA = "ventas_limpias.csv"

try:
    # === 📂 Validación de existencia ===
    if not os.path.exists(ENTRADA):
        raise FileNotFoundError(f"❌ El archivo '{ENTRADA}' no fue encontrado.")

    # === 📥 Cargar datos desde CSV ===
    df = pd.read_csv(ENTRADA)

    # === ✅ Validar estructura de columnas ===
    esperadas = ['fecha', 'producto', 'ventas', 'region']
    if list(df.columns) != esperadas:
        raise ValueError(f"❌ Columnas inválidas. Se esperaban: {esperadas}, se recibieron: {list(df.columns)}")

    # === 🔄 Conversión de tipos ===
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce')

    # === 🧹 Eliminar nulos ===
    df.dropna(inplace=True)

    # === 📊 Detección de outliers por IQR ===
    Q1 = df['ventas'].quantile(0.25)
    Q3 = df['ventas'].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR

    antes = len(df)
    df = df[(df['ventas'] >= lim_inf) & (df['ventas'] <= lim_sup)]
    despues = len(df)

    # === 💾 Guardar archivo limpio ===
    df.to_csv(SALIDA, index=False)

    # === 📋 Log final ===
    print(f"✅ Limpieza completada: {SALIDA}")
    print(f"🧾 Registros antes: {antes} | después: {despues} | eliminados: {antes - despues}")
    sys.exit(0)

except Exception as e:
    print(f"❌ Error en limpieza de datos: {str(e)}")
    sys.exit(1)

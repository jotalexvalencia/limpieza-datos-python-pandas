import pandas as pd
import sys
import os



from scripts.process_data import limpiar_datos

def test_eliminar_outliers():
    # 1. SETUP: Creamos datos falsos con un outlier obvio
    data = {
        'fecha': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'producto': ['A', 'B', 'C', 'D', 'E'],
        'ventas': [100, 110, 105, 120, 1000], # 1000 es el Outlier
        'region': ['Norte', 'Sur', 'Este', 'Oeste', 'Norte']
    }
    df = pd.DataFrame(data)

    # 2. EJECUCIÓN
    df_limpio = limpiar_datos(df)

    # 3. VERIFICACIÓN (ASSERT)
    assert len(df_limpio) == 4, "Debería haber eliminado el outlier de 1000"
    assert 1000 not in df_limpio['ventas'].values, "El valor 1000 no debe estar presente"
    
def test_estructura_invalida():
    # Verificamos que falle si faltan columnas
    data = { 'fecha': ['2023-01-01'], 'producto': ['A'] } # Faltan 'ventas' y 'region'
    df = pd.DataFrame(data)
    
    # Esperamos que lance un ValueError
    try:
        limpiar_datos(df)
        assert False, "Debería haber lanzado un error por columnas faltantes"
    except ValueError:
        assert True
import pandas as pd # Librería para análisis de datos

# cargar datos desde un archivo csv
data = pd.read_csv("ventas.csv")

# Detectar outliers con IQR (método más robusto)  
Q1 = data['ventas'].quantile(0.25)  # Primer cuartil
Q3 = data['ventas'].quantile(0.75)  # Tercer cuartil  
IQR = Q3 - Q1  # Rango intercuartílico
lower = Q1 - 1.5 * IQR  # Límite inferior
upper = Q3 + 1.5 * IQR  # Límite superior 

print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}, lower: {lower}, upper: {upper}")

# Filtrar datos
cleaned = data[(data['ventas'] >= lower) & (data['ventas'] <= upper)]

# guardar datos limpios en un archivo csv
cleaned.to_csv('ventas_limpias.csv', index=False)
print(f"Se eliminaron {len(data) - len(cleaned)} outliers.")
# === 📦 Importaciones necesarias ===
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
import base64
import shutil
import subprocess
from pathlib import Path

# === 🚀 Inicializamos la app FastAPI ===
app = FastAPI()

# === 📁 Montaje del frontend en /static y carga directa del index en /
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend", html=False), name="static")

@app.get("/")
def serve_index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

# === 📍 Variables de ruta ===
CSV_PATH = "ventas_limpias.csv"
IMG_PATH = "assets/images/boxplot_despues.png"
UPLOADS_DIR = "uploads/"
RAW_CSV_NAME = "ventas.csv"

# === 📤 Endpoint POST: /upload ===
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(content={"error": "Solo se permiten archivos .csv"}, status_code=400)

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    temp_path = os.path.join(UPLOADS_DIR, file.filename)

    # Guardamos el archivo temporalmente
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Intentamos leer el CSV
    try:
        df = pd.read_csv(temp_path, sep=",")
    except Exception as e:
        return JSONResponse(content={"error": f"No se pudo leer el CSV: {str(e)}"}, status_code=422)

    # Validamos columnas esperadas
    columnas_esperadas = ['fecha', 'producto', 'ventas', 'region']
    if list(df.columns) != columnas_esperadas:
        return JSONResponse(
            content={"error": f"Columnas inválidas. Se esperaban: {columnas_esperadas}, se recibieron: {list(df.columns)}"},
            status_code=422
        )

    # Conversión de tipos
    try:
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
        df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce')
    except Exception as e:
        return JSONResponse(content={"error": f"Error de tipo en columnas: {str(e)}"}, status_code=422)

    df.dropna(inplace=True)

    # === 🧹 Manejo de archivo original ===
    try:
        if os.path.exists(RAW_CSV_NAME):
            os.remove(RAW_CSV_NAME)
            print("✅ Archivo ventas.csv eliminado correctamente.")
        else:
            print("ℹ️ No existía ventas.csv, no fue necesario eliminarlo.")

        os.rename(temp_path, RAW_CSV_NAME)
        print("✅ Archivo temporal renombrado a ventas.csv.")
    except Exception as e:
        print("❌ Error al manejar archivos CSV:", e)
        return JSONResponse(content={"error": f"Error al preparar archivo CSV: {str(e)}"}, status_code=500)

    # === 🧪 Ejecutamos el script de limpieza ===
    try:
        subprocess.run(["python", "scripts/process_data.py"], check=True)
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": f"Error al ejecutar la limpieza: {str(e)}"}, status_code=500)

    # === 📊 Verificamos archivo limpio ===
    if os.path.exists(CSV_PATH):
        df_limpio = pd.read_csv(CSV_PATH)
        registros_final = len(df_limpio)
    else:
        return JSONResponse(content={"error": "Archivo limpio no encontrado"}, status_code=500)

    return {
        "mensaje": f"Archivo subido y procesado exitosamente: {file.filename}",
        "filas_finales": registros_final,
        "archivo_salida": CSV_PATH
    }

# === 📥 Endpoint GET: /datos ===
@app.get("/datos")
def obtener_datos(limit: int = 100):
    MAX_LIMIT = 1000
    if limit > MAX_LIMIT:
        return JSONResponse(content={"error": f"Límite máximo: {MAX_LIMIT}"}, status_code=400)

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df.head(limit).to_dict(orient="records")

    return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)

# === 📈 Endpoint GET: /resumen ===
@app.get("/resumen")
def resumen_estadistico():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df.describe().to_dict()

    return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)

# === 🖼️ Endpoint GET: /grafico ===
@app.get("/grafico")
def grafico_base64():
    if os.path.exists(IMG_PATH):
        with open(IMG_PATH, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return {"imagen_base64": encoded}

    return JSONResponse(content={"error": "Imagen no encontrada"}, status_code=404)

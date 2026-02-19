### Limpieza de Datos con Python y Pandas (ETL Pipeline)
![1771530591706](image/README/1771530591706.png)
![1771530602772](image/README/1771530602772.png)
![1771530629100](image/README/1771530629100.png)
![1771530640664](image/README/1771530640664.png)

## 📝 Descripción
Pipeline de datos automatizado (ETL: Extract, Transform, Load) diseñado para la limpieza de datasets mediante el método estadístico IQR (Rango Intercuartílico) para la detección y eliminación de outliers.

Este proyecto implementa una API REST con FastAPI para la gestión web y un pipeline de CI/CD con GitHub Actions para cargar automáticamente los datos procesados a un bucket de AWS S3.

Casos de uso:

Preparación de datos para análisis financiero y auditorías.
Limpieza automatizada de datos crudos antes de ingestas en Data Warehouses.
Ejemplo práctico de arquitectura serverless y automatización de tareas.

## 🏗️ Arquitectura del Proyecto
Flujo de datos desde la fuente local hasta el almacenamiento en la nube:

```mermaid
flowchart LR
    A["📁 Dataset Local: ventas.csv"] -->|Input| B("🐍 Script Python: process_data.py")
    B -->|Lógica: IQR & Pandas| C["📊 Dataset Limpio: ventas_limpias.csv"]
    C -->|Git Push| D["🐙 GitHub Repository"]
    D -->|Trigger| E{"⚙️ GitHub Actions"}
    E -->|Config Creds| F["☁️ AWS S3 Bucket"]
    F -->|Output Final| G["✅ Archivo Procesado en la Nube"]

    %% Styles
    classDef py fill:#3776ab,stroke:#333,stroke-width:2px,color:#fff;
    classDef gha fill:#2088FF,stroke:#333,stroke-width:2px,color:#fff;
    classDef s3 fill:#FF9900,stroke:#333,stroke-width:2px,color:#fff;
    class B py;
    class E gha;
    class F s3;
```

## 🚀 Tecnologías Utilizadas
- Python: Lenguaje principal para la lógica de procesamiento.
- Pandas: Librería para manipulación y análisis de datos.
- FastAPI: Framework para la construcción de APIs REST.
- AWS S3: Almacenamiento de objetos escalable (Data Lake).
- Boto3: SDK de AWS para Python.
- GitHub Actions: Automatización de flujos de trabajo (CI/CD).

## 📂 Estructura del Proyecto

LIMPIEZA_DATOS/
├── .github/
│   └── workflows/
│       └── deploy-to-s3.yml   # Configuración CI/CD
├── assets/
│   └── images/                # Diagramas y boxplots generados
├── frontend/                  # Interfaz web estática
├── scripts/                   
│   ├── process_data.py        # Script principal (ETL)
│   └── graficar_boxplot.py    # Script de visualización
├── uploads/                   # Carpeta de entrada temporal
├── main.py                    # Servidor FastAPI (Orquestador)
├── .gitignore                 # Archivos ignorados por Git
├── ventas.csv                 # Dataset de entrada (Raw)
├── ventas_limpias.csv         # Dataset procesado (Clean)
├── requirements.txt           # Dependencias del proyecto
└── README.md

## ⚙️ Instalación y Configuración
1. Clonar el Repositorio
git clone https://github.com/jotalexvalencia/limpieza-datos-python-pandas.git
cd limpieza-datos-python-pandas
2. Crear Entorno Virtual (recomendado)
   # Windows
    python -m venv env
    env\Scripts\activate

    # macOS/Linux
    python3 -m venv env
    source env/bin/activate
3. Instalar Dependencias
   pip install -r requirements.txt
4. Configuración de AWS
   Asegúrate de tener configuradas tus credenciales de AWS localmente o como Secrets en tu repositorio de GitHub (AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY).

## 🛠️ Uso

# Opción A: Ejecutar la API Web (Recomendado)

1. Inicia el servidor:
uvicorn main:app --reload

2. Abre tu navegador en http://127.0.0.1:8000.
3. Usa la interfaz para subir tu archivo ventas.csv.
   
# Opción B: Ejecutar Script Manualmente

1. Coloca tu archivo de datos crudos en la raíz con el nombre ventas.csv.
2. Ejecuta el script de limpieza:
python scripts/process_data.py
3. Se generará ventas_limpias.csv.

## 🤖 Automatización (CI/CD)

Este proyecto utiliza GitHub Actions para desplegar automáticamente el archivo procesado a AWS S3 cada vez que se realiza un push a la rama dev-python.

Flujo del workflow:

Checkout: Descarga el código del repositorio.
Setup: Configura las credenciales de AWS de forma segura usando Secrets.
Deploy: Sube el archivo ventas_limpias.csv al bucket S3 especificado.

## 📊 Ejemplo de Lógica (IQR)
El script utiliza el Rango Intercuartílico para filtrar datos anómalos:

1. Calcular Q1 (25%) y Q3 (75%).
2. Obtener IQR = Q3 - Q1.
3. Definir límites:
   - Inferior: Q1 - 1.5 * IQR
   - Superior: Q3 + 1.5 * IQR
4. Mantener solo los datos dentro de esos límites.
   
## 👤 Autor
Jorge Alexander Valencia Valencia
[LinkedIn](https://www.linkedin.com/in/jorgealexandervalencia/) | [GitHub](https://github.com/jotalexvalencia)

## 📄 Licencia
Este proyecto está bajo la Licencia MIT.
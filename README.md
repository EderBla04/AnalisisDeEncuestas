# Análisis de Encuestas

Una aplicación de escritorio para analizar datos de encuestas en formato CSV, desarrollada con PyQt6.

## Características

- Carga de archivos CSV
- Resumen estadístico de las respuestas
- Generación de gráficas de pastel y barras
- Interfaz gráfica moderna y fácil de usar
- Exportación de gráficas en formato PNG o JPG

## Estructura del Proyecto (MVC)

El proyecto sigue el patrón de diseño Modelo-Vista-Controlador (MVC):

- **models/**: Contiene la lógica de negocio y manejo de datos
  - `survey_model.py`: Maneja la carga y procesamiento de datos CSV
  
- **views/**: Contiene las interfaces de usuario
  - `main_window.py`: Ventana principal de la aplicación
  - `MainWindow.ui`: Archivo de diseño de la interfaz

- **controllers/**: Contiene la lógica de control
  - `survey_controller.py`: Coordina la interacción entre el modelo y la vista

- **utils/**: Contiene utilidades generales
  - `loading_progress.py`: Widget de progreso personalizado

## Requisitos

- Python 3.8 o superior
- Las dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecutar la aplicación:
   ```bash
   python main.py
   ```
2. Usar el botón "Cargar CSV" para seleccionar un archivo de datos
3. Utilizar los botones de la interfaz para generar resúmenes y gráficas
4. Las gráficas generadas se pueden guardar usando el botón "Guardar Gráfica"

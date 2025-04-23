import os
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog,
    QInputDialog, QWidget, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from controllers.survey_controller import SurveyController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "MainWindow.ui")
        loadUi(ruta_ui, self)

        # Controlador
        self.controller = SurveyController()
        
        # Estado de la UI
        self.canvas = None
        self.current_figure = None
        
        # Widgets
        self.txtResumen = self.findChild(QTextEdit, "txtResumen")
        self.lblNoData = self.findChild(QWidget, "lblNoData")

        # Conexiones
        self.setup_connections()
        
        # Estado inicial de botones
        self._actualizar_estado_botones(False)

    def setup_connections(self):
        """Configura las conexiones de señales y slots"""
        self.btnCargarCSV.clicked.connect(self.cargar_csv)
        self.btnResumen.clicked.connect(self.mostrar_resumen)
        self.btnGraficaPastel.clicked.connect(lambda: self.generar_grafica("pastel"))
        self.btnGraficaBarras.clicked.connect(lambda: self.generar_grafica("barras"))
        self.btnGuardarGrafica.clicked.connect(self.guardar_grafica)

    def _actualizar_estado_botones(self, habilitado: bool):
        """Actualiza el estado de los botones según si hay datos cargados"""
        self.btnResumen.setEnabled(habilitado)
        self.btnGraficaPastel.setEnabled(habilitado)
        self.btnGraficaBarras.setEnabled(habilitado)
        self.btnGuardarGrafica.setEnabled(False)

    def cargar_csv(self):
        """Maneja la carga de archivos CSV"""
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not ruta:
            return
        
        try:
            self.controller.load_csv(ruta)
            QMessageBox.information(
                self, "Éxito", f"Archivo cargado:\n{os.path.basename(ruta)}"
            )
            self._actualizar_estado_botones(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self._actualizar_estado_botones(False)

    def mostrar_resumen(self):
        """Muestra el resumen de los datos"""
        if self.canvas is not None:
            self.canvas.hide()
        self.lblNoData.hide()
        
        resumen = self.controller.get_summary()
        self.txtResumen.setPlainText(resumen)
        self.txtResumen.setVisible(True)
        self.btnGuardarGrafica.setEnabled(False)

    def _seleccionar_columna(self):
        """Muestra un diálogo para seleccionar una columna"""
        columnas = self.controller.get_columns()
        columna, ok = QInputDialog.getItem(
            self, "Seleccionar pregunta", "Pregunta:", columnas, 0, False
        )
        return columna if ok else None

    def generar_grafica(self, tipo):
        """Genera una gráfica según el tipo especificado"""
        col = self._seleccionar_columna()
        if col is None:
            return

        # Ocultar elementos
        self.txtResumen.setVisible(False)
        self.lblNoData.hide()

        # Limpiar gráfica anterior
        if self.canvas is not None:
            self.graphContainer.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        # Generar nueva gráfica
        self.current_figure = self.controller.generate_chart(col, tipo)
        if self.current_figure is None:
            return

        # Mostrar gráfica
        self.canvas = FigureCanvas(self.current_figure)
        layout = self.graphContainer.layout()
        layout.insertWidget(0, self.canvas)
        self.canvas.draw()

        # Habilitar botón de guardar
        self.btnGuardarGrafica.setEnabled(True)

    def guardar_grafica(self):
        """Guarda la gráfica actual en un archivo"""
        if not self.current_figure:
            return
            
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar gráfica", "", "PNG Files (*.png);;JPEG (*.jpg);;All Files (*)"
        )
        if not ruta:
            return
            
        try:
            self.controller.save_chart(self.current_figure, ruta)
            QMessageBox.information(
                self, "Guardado", f"Gráfica guardada en:\n{ruta}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

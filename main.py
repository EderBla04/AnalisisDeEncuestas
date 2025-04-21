import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QFileDialog, QInputDialog, QWidget, QTextEdit,
    QSplashScreen, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.uic import loadUi

class BotonesVista(QMainWindow):

    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "MainWindow.ui")
        loadUi(ruta_ui, self)

        # Estado inicial
        self.df = None
        self.fig = None
        self.canvas = None

        # Guardar referencias a widgets importantes
        self.txtResumen = self.findChild(QTextEdit, "txtResumen")
        self.lblNoData = self.findChild(QWidget, "lblNoData")

        # Conexiones
        self.btnCargarCSV.clicked.connect(self.cargar_csv)
        self.btnResumen.clicked.connect(self.mostrar_resumen)
        self.btnGraficaPastel.clicked.connect(lambda: self.generar_grafica("pastel"))
        self.btnGraficaBarras.clicked.connect(lambda: self.generar_grafica("barras"))
        self.btnGuardarGrafica.clicked.connect(self.guardar_grafica)

        # Estado inicial de botones
        self._actualizar_estado_botones(False)

    def _actualizar_estado_botones(self, habilitado: bool):
        """Actualiza el estado de los botones según si hay datos cargados"""
        self.btnResumen.setEnabled(habilitado)
        self.btnGraficaPastel.setEnabled(habilitado)
        self.btnGraficaBarras.setEnabled(habilitado)
        self.btnGuardarGrafica.setEnabled(False)  # Este se habilita solo al generar gráfica

    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not ruta:
            return
        
        try:
            self.df = pd.read_csv(ruta)
            QMessageBox.information(
                self, "Éxito", f"Archivo cargado:\n{os.path.basename(ruta)}"
            )
            self._actualizar_estado_botones(True)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo cargar el CSV:\n{str(e)}"
            )
            self.df = None
            self._actualizar_estado_botones(False)

    def mostrar_resumen(self):
        # Ocultar gráfica si existe
        if self.canvas is not None:
            self.canvas.hide()
        self.lblNoData.hide()
        
        # Construir texto de resumen
        resumen = ""
        for col in self.df.columns:
            resumen += f"== Pregunta: {col} ==\n"
            counts = self.df[col].value_counts(dropna=False)
            for val, cnt in counts.items():
                resumen += f"  • {val}: {cnt}\n"
            resumen += "\n"

        # Mostrar en el QTextEdit
        self.txtResumen.setPlainText(resumen)
        self.txtResumen.setVisible(True)
        self.btnGuardarGrafica.setEnabled(False)

    def _seleccionar_columna(self):
        columna, ok = QInputDialog.getItem(
            self, "Seleccionar pregunta", "Pregunta:", list(self.df.columns), 0, False
        )
        return columna if ok else None

    def generar_grafica(self, tipo):
        col = self._seleccionar_columna()
        if col is None:
            return

        # Ocultar resumen y label
        self.txtResumen.setVisible(False)
        self.lblNoData.hide()

        # Limpiar gráfica anterior si existe
        if self.canvas is not None:
            self.graphContainer.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        # Crear nueva figura con tamaño más grande
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='#27293d')
        ax = self.fig.add_subplot(111)
        
        # Configurar estilo de la figura
        ax.set_facecolor('#27293d')
        ax.tick_params(colors='white', labelsize=12)  # Aumentar tamaño de las etiquetas de los ejes
        for spine in ax.spines.values():
            spine.set_color('white')

        # Generar gráfica según tipo
        counts = self.df[col].value_counts()
        if tipo == "pastel":
            wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
            # Configurar el tamaño y color de las etiquetas
            plt.setp(autotexts, size=14, color='white', weight='bold')  # Porcentajes
            plt.setp(texts, size=14, color='white', weight='bold')      # Etiquetas
            ax.set_title(f"Distribución de respuestas: {col}", color='white', pad=20, fontsize=16, weight='bold')
        else:  # gráfica de barras
            bars = ax.bar(range(len(counts)), counts.values)
            ax.set_title(f"Respuestas por categoría: {col}", color='white', pad=20, fontsize=16, weight='bold')
            ax.set_ylabel("Conteo", color='white', fontsize=14, weight='bold')
            ax.set_xlabel(col, color='white', fontsize=14, weight='bold')
            
            # Configurar etiquetas del eje X
            ax.set_xticks(range(len(counts)))
            ax.set_xticklabels(counts.index, rotation=45, ha='right', fontsize=12)
            
            # Ajustar color de las barras y agregar valores encima
            for i, bar in enumerate(bars):
                bar.set_color('#2196F3')  # Usar el mismo azul de los botones
                # Agregar el valor encima de cada barra
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', color='white', 
                       fontsize=12, weight='bold')

        # Ajustar layout para que todo quepa bien
        self.fig.tight_layout()

        # Crear canvas y agregarlo al contenedor
        self.canvas = FigureCanvas(self.fig)
        layout = self.graphContainer.layout()
        layout.insertWidget(0, self.canvas)
        self.canvas.draw()

        # Habilitar botón de guardar
        self.btnGuardarGrafica.setEnabled(True)

    def guardar_grafica(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar gráfica", "", "PNG Files (*.png);;JPEG (*.jpg);;All Files (*)"
        )
        if not ruta:
            return
            
        try:
            self.fig.savefig(ruta, facecolor=self.fig.get_facecolor(), bbox_inches='tight')
            QMessageBox.information(
                self, "Guardado", f"Gráfica guardada en:\n{ruta}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo guardar la gráfica:\n{str(e)}"
            )


class LoadingProgress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(30, 30))
        
        self.setTextVisible(False)
        self.setRange(0, 0)  # Modo indeterminado
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 15px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: transparent;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Cargar y redimensionar el logo
    logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "assets", "Logo App.png"))
    logo_size = 150  # Tamaño fijo más pequeño
    logo_pixmap = logo_pixmap.scaled(logo_size, logo_size, Qt.AspectRatioMode.KeepAspectRatio)
    
    # Crear un pixmap más grande para el fondo
    splash_pixmap = QPixmap(logo_size + 30, logo_size + 60)  # Espacio extra reducido
    splash_pixmap.fill(Qt.GlobalColor.white)
    
    # Dibujar el logo en el centro del fondo
    painter = QPainter(splash_pixmap)
    painter.drawPixmap((splash_pixmap.width() - logo_pixmap.width()) // 2, 10, logo_pixmap)
    painter.end()
    
    # Crear el splash screen
    splash = QSplashScreen(splash_pixmap)
    splash.setStyleSheet("""
        QSplashScreen {
            border: 2px solid #cccccc;
            border-radius: 10px;
        }
    """)
    
    # Crear y posicionar el círculo de progreso
    progress = LoadingProgress(splash)
    progress.move((splash_pixmap.width() - progress.width()) // 2, 
                 splash_pixmap.height() - progress.height() - 15)
    
    # Mostrar mensaje de carga
    splash.showMessage("Cargando...", 
                      Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, 
                      QColor("#333333"))
    splash.show()
    progress.show()
    
    # Procesar eventos para asegurar que se muestre el splash
    app.processEvents()
    
    # Simular tiempo de carga
    timer = QTimer()
    timer.singleShot(2000, lambda: None)  # Esperar 2 segundos
    
    # Crear la ventana principal
    ventana = BotonesVista()
    
    # Mostrar la ventana principal y cerrar el splash
    ventana.show()
    splash.finish(ventana)
    
    sys.exit(app.exec())

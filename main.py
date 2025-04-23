import sys
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QPainter
from views.main_window import MainWindow
from utils.loading_progress import LoadingProgress

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
    ventana = MainWindow()
    
    # Mostrar la ventana principal y cerrar el splash
    ventana.show()
    splash.finish(ventana)
    
    sys.exit(app.exec())

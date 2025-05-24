#!/usr/bin/env python3
"""
Extractor de Código - Aplicación Principal
Aplicación GUI para extraer y consolidar código de proyectos en un archivo de texto.
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QFrame, QTextEdit, QStatusBar, QLineEdit
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QIcon, QColor, QPalette
from PySide6.QtCore import Qt, QTimer
from core.file_extractor import FileExtractor
from config import DEFAULT_OUTPUT_FILENAME, DEFAULT_LOG_FILENAME
import os

class DragDropFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        
        # Estilo inicial más limpio
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #4e8cff;
                border-radius: 15px;
                background-color: #f8f9fa;
                min-height: 180px;
                max-height: 180px;
            }
            QFrame:hover {
                border-color: #357ae8;
                background-color: #eef3ff;
            }
        """)
        
        # Layout principal perfectamente centrado con QVBoxLayout y addStretch
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(2)  # Espaciado mínimo entre icono y texto

        # Icono (más grande)
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignHCenter)
        self.icon_label.setFont(QFont("Segoe UI Emoji", 28))
        self.icon_label.setStyleSheet("color: #4e8cff; background: transparent; border: none;")

        # Texto principal (HTML para salto de línea y centrado)
        self.folder_name = QLabel("<div style='text-align:center;'>Arrastra una carpeta aquí<br>o haz clic para buscar</div>")
        self.folder_name.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.folder_name.setAlignment(Qt.AlignHCenter)
        self.folder_name.setStyleSheet("color: #333; background: transparent; border: none;")
        self.folder_name.setTextFormat(Qt.RichText)
        self.folder_name.setWordWrap(True)
        self.folder_name.setMinimumHeight(32)

        # Ruta del archivo (inicialmente oculta)
        self.folder_path = QLabel("")
        self.folder_path.setFont(QFont("Segoe UI", 8))
        self.folder_path.setAlignment(Qt.AlignHCenter)
        self.folder_path.setStyleSheet("color: #666; background: transparent; border: none;")
        self.folder_path.setWordWrap(True)
        self.folder_path.setVisible(False)

        layout.addStretch(1)
        layout.addWidget(self.icon_label, 0, Qt.AlignHCenter)
        layout.addWidget(self.folder_name, 0, Qt.AlignHCenter)
        layout.addWidget(self.folder_path, 0, Qt.AlignHCenter)
        layout.addStretch(2)

        self.setLayout(layout)

        self.file_path = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # Cambio visual al arrastrar
            self.setStyleSheet("""
                QFrame {
                    border: 2px solid #28a745;
                    border-radius: 15px;
                    background-color: #d4edda;
                    min-height: 180px;
                    max-height: 180px;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # Volver al estilo original
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #4e8cff;
                border-radius: 15px;
                background-color: #f8f9fa;
                min-height: 180px;
                max-height: 180px;
            }
            QFrame:hover {
                border-color: #357ae8;
                background-color: #eef3ff;
            }
        """)

    def dropEvent(self, event: QDropEvent):
        # Volver al estilo original
        self.dragLeaveEvent(event)
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()
                if os.path.isdir(path):
                    self.file_path = path
                    self.update_display(path)
                else:
                    self.show_error("❌ Solo se permiten carpetas")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            dlg = QFileDialog(self, "Seleccionar carpeta")
            dlg.setFileMode(QFileDialog.Directory)
            if dlg.exec():
                folders = dlg.selectedFiles()
                if folders:
                    path = folders[0]
                    self.file_path = path
                    self.update_display(path)
    
    def update_display(self, path):
        """Actualiza la visualización cuando se selecciona una carpeta"""
        folder_name = os.path.basename(path)
        
        # Cambiar icono y texto - MANTENER TAMAÑO PEQUEÑO
        self.icon_label.setText("✅")
        self.icon_label.setFont(QFont("Segoe UI Emoji", 36))  # Mantener el mismo tamaño
        self.folder_name.setText(f"Carpeta seleccionada: {folder_name}")
        
        # Mostrar ruta (truncada si es muy larga)
        display_path = path
        if len(display_path) > 60:
            display_path = "..." + display_path[-57:]
        
        self.folder_path.setText(display_path)
        self.folder_path.setVisible(True)
        self.folder_path.setMaximumHeight(25)  # Altura más compacta
        
        # Cambiar estilo para mostrar que está seleccionada
        self.setStyleSheet("""
            QFrame {
                border: 2px solid #28a745;
                border-radius: 15px;
                background-color: #d4edda;
                min-height: 180px;
                max-height: 180px;
            }
        """)
    
    def show_error(self, message):
        """Muestra un mensaje de error temporal"""
        self.icon_label.setText("❌")
        self.icon_label.setFont(QFont("Segoe UI Emoji", 36))  # Mantener el mismo tamaño
        self.folder_name.setText(message)
        self.folder_path.setVisible(False)
        self.folder_path.setMaximumHeight(0)
        
        # Timer para volver al estado original después de 3 segundos
        QTimer.singleShot(3000, self.reset_display)
    
    def reset_display(self):
        """Resetea la visualización al estado inicial"""
        self.file_path = None
        self.icon_label.setText("📁")
        self.icon_label.setFont(QFont("Segoe UI Emoji", 36))  # Mantener el mismo tamaño
        self.folder_name.setText("Arrastra una carpeta aquí o haz clic para buscar")
        self.folder_path.setText("")
        self.folder_path.setVisible(False)
        self.folder_path.setMaximumHeight(0)
        
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #4e8cff;
                border-radius: 15px;
                background-color: #f8f9fa;
                min-height: 180px;
                max-height: 180px;
            }
            QFrame:hover {
                border-color: #357ae8;
                background-color: #eef3ff;
            }
        """)

class ExtractorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extractor de Código (PySide6)")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "app_icon.ico")))
        self.setMinimumSize(700, 500)
        self.extractor = FileExtractor()
        self.current_source_path = ""
        self.current_output_path = DEFAULT_OUTPUT_FILENAME
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 10)
        layout.setSpacing(18)

        title = QLabel("Extractor de Código")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Consolida todo el código de tu proyecto en un archivo de texto")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #4e8cff;")
        layout.addWidget(subtitle)

        self.drop_frame = DragDropFrame()
        layout.addWidget(self.drop_frame)

        # Output section elegante
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Archivo de salida:"))
        self.output_entry = QLineEdit()
        self.output_entry.setText(DEFAULT_OUTPUT_FILENAME)
        self.output_entry.setMinimumWidth(320)
        self.output_entry.setStyleSheet("QLineEdit { border: 2px solid #4e8cff; border-radius: 8px; padding: 4px 8px; font-size: 13px; }")
        output_layout.addWidget(self.output_entry)
        btn_browse = QPushButton("📂")
        btn_browse.setToolTip("Buscar archivo de salida")
        btn_browse.setFixedWidth(36)
        btn_browse.setStyleSheet("QPushButton { background: #eaf1fb; border-radius: 8px; font-size: 18px; } QPushButton:hover { background: #d5f5e3; }")
        btn_browse.clicked.connect(self.select_output_file)
        output_layout.addWidget(btn_browse)
        layout.addLayout(output_layout)

        # Action buttons modernos
        btn_layout = QHBoxLayout()
        self.btn_extract = QPushButton("🚀 Extraer Código")
        self.btn_extract.setStyleSheet("QPushButton { background: #4e8cff; color: white; border-radius: 12px; font-size: 15px; padding: 8px 20px; } QPushButton:hover { background: #357ae8; }")
        self.btn_extract.setMinimumHeight(36)
        self.btn_extract.clicked.connect(self.start_extraction)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_extract)
        self.btn_clear = QPushButton("🗑️ Limpiar")
        self.btn_clear.setStyleSheet("QPushButton { background: #f2f2f2; color: #444; border-radius: 12px; font-size: 15px; padding: 8px 20px; } QPushButton:hover { background: #ffe0e0; }")
        self.btn_clear.setMinimumHeight(36)
        self.btn_clear.clicked.connect(self.clear_selection)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo para extraer código")

        self.setCentralWidget(central)

    def select_output_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de código extraído", self.output_entry.text(), "Archivos de texto (*.txt)")
        if path:
            self.output_entry.setText(path)

    def start_extraction(self):
        folder = self.drop_frame.file_path
        output_path = self.output_entry.text().strip()
        if not folder:
            self.status.showMessage("Selecciona una carpeta primero", 5000)
            return
        if not output_path:
            self.status.showMessage("Especifica un archivo de salida", 5000)
            return
        try:
            log_path = os.path.join(os.path.dirname(output_path), DEFAULT_LOG_FILENAME)
            processed_files, errors = self.extractor.extract_content(folder, output_path, log_path)
            msg = f"Extracción completada. Archivos: {processed_files}. Errores: {len(errors)}. Guardado en: {output_path}"
            self.status.showMessage(msg, 10000)
        except Exception as e:
            self.status.showMessage(f"Error: {str(e)}", 10000)

    def clear_selection(self):
        # Usar el método reset_display de DragDropFrame
        self.drop_frame.reset_display()
        self.output_entry.setText(DEFAULT_OUTPUT_FILENAME)
        self.status.showMessage("Listo para extraer código", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ExtractorWindow()
    win.show()
    sys.exit(app.exec())
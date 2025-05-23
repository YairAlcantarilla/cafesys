import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

class DiagnosticoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnóstico del Sistema")
        self.setFixedSize(800, 600)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        layout.addWidget(self.text_log)
        
        btn_check = QPushButton("Ejecutar Diagnóstico")
        btn_check.clicked.connect(self.run_diagnostics)
        layout.addWidget(btn_check)

    def run_diagnostics(self):
        self.text_log.clear()
        self.log("Iniciando diagnóstico...")
        
        # Verificar Python y entorno
        self.log(f"Python versión: {sys.version}")
        self.log(f"Path de Python: {sys.executable}")
        self.log(f"Directorio actual: {os.getcwd()}")
        
        # Verificar módulos
        self.log("\nVerificando módulos:")
        modules = ["PyQt6", "mysql.connector", "PIL", "qrcode", "cv2", "pyzbar"]
        for module in modules:
            try:
                __import__(module)
                self.log(f"✓ {module} - Instalado correctamente")
            except ImportError as e:
                self.log(f"✗ {module} - No instalado: {str(e)}")
        
        # Verificar archivos de imagen
        self.log("\nVerificando archivos de imagen:")
        image_paths = [
            "imagenes/fondomenu1.png",
            "imagenes/Mpersonal.png",
            "imagenes/CAFESYSNUEVO.png",
            "imagenes/PAJUSTES.png",
            "imagenes/plantilla_gafete.png"
        ]
        for path in image_paths:
            if os.path.exists(path):
                self.log(f"✓ {path} - Existe")
            else:
                self.log(f"✗ {path} - No existe")
        
        # Verificar conexión a base de datos
        self.log("\nVerificando conexión a base de datos:")
        try:
            from conexion import conectar_db
            conn = conectar_db()
            if conn:
                self.log("✓ Conexión a la base de datos exitosa")
                conn.close()
            else:
                self.log("✗ No se pudo conectar a la base de datos")
        except Exception as e:
            self.log(f"✗ Error de conexión: {str(e)}")
            self.log(traceback.format_exc())

    def log(self, message):
        self.text_log.append(message)
        print(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiagnosticoWindow()
    window.show()
    sys.exit(app.exec())
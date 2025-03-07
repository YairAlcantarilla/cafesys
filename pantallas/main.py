import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from p_inicio import PInicio

class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 400)
        
        layout = QVBoxLayout()
        
        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("logo.png")  # Asegúrate de que el archivo exista en el mismo directorio
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(150, 150)
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Campos de usuario y contraseña
        self.usuario = QLineEdit(self)
        self.usuario.setPlaceholderText("Usuario")
        layout.addWidget(self.usuario)
        
        self.contraseña = QLineEdit(self)
        self.contraseña.setPlaceholderText("Contraseña")
        self.contraseña.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.contraseña)
        
        # Botón de inicio de sesión
        self.boton_iniciar = QPushButton("Iniciar Sesión", self)
        self.boton_iniciar.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.boton_iniciar)
        
        self.setLayout(layout)
    
    def iniciar_sesion(self):
        # Aquí puedes agregar validaciones de usuario y contraseña
        self.ventana_principal = PInicio()
        self.ventana_principal.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    sys.exit(app.exec())

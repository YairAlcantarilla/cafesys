import sys
import os
import p_inicio

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAFESYS - Login")
        self.setFixedSize(320, 420)
        self.setStyleSheet("background-color: #0D1321;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ###################
        self.logo_label = QLabel(self)
        ruta_imagen = "./imagenes/logo.png"  
        pixmap = QPixmap(ruta_imagen)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.logo_label.setPixmap(pixmap)
        else:
            print("Error: La imagen no se pudo cargar.")
        
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)
        #####################
    
        self.user_label = QLabel("ID de usuario")
        self.user_label.setStyleSheet("color: white;")
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("background-color: white; color:black; border-radius: 10px; padding: 5px;")
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        
        self.pass_label = QLabel("Contraseña")
        self.pass_label.setStyleSheet("color: white;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 5px;")
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)

        
        self.login_button = QPushButton("Acceder")
        self.login_button.setStyleSheet(
            "background-color: white; color: black; border-radius: 10px; padding: 10px; font-weight: bold;"
        )
        self.login_button.clicked.connect(self.check_login)  
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        usuario = self.user_input.text()
        contraseña = self.pass_input.text()

        if usuario == "admin" and contraseña == "1234":
            self.main_window = p_inicio.MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

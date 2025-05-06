import sys
import os
import p_inicio
import Caja
import cv2
from pyzbar.pyzbar import decode
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                           QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer
from conexion import verificar_credenciales
# Add import for set_current_user function
from globals import set_current_user

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAFESYS - Login")
        self.setFixedSize(320, 520)  # Aumentado el alto para el botón QR
        self.setStyleSheet("background-color: #0D1321;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ###################
        self.logo_label = QLabel(self)
        ruta_imagen = "./imagenes/CAFESYSNUEVO.png"  
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

        # Agregar botón para escanear QR
        self.qr_button = QPushButton("Iniciar sesión con QR")
        self.qr_button.setStyleSheet(
            "background-color: white; color: black; border-radius: 10px; padding: 10px; font-weight: bold;"
        )
        self.qr_button.clicked.connect(self.open_qr_scanner)
        layout.addWidget(self.qr_button)

        self.setLayout(layout)
        
        # Variables para el escaneo QR
        self.camera = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def check_login(self):
        usuario = self.user_input.text()
        contraseña = self.pass_input.text()

        if not usuario or not contraseña:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return

        resultado = verificar_credenciales(usuario, contraseña)

        if resultado and len(resultado) == 3:
            id_usuario, nombre, id_puesto = resultado
            
            # Set the current user name in globals
            set_current_user(nombre)
            
            try:
                # Convertir id_puesto a entero para comparación
                id_puesto = int(id_puesto)
                
                if id_puesto == 1:  # Administrador
                    self.main_window = p_inicio.MainWindow()
                    self.main_window.show()
                else:  # Cualquier otro ID irá a Caja
                    self.main_window = Caja.CajaI()
                    self.main_window.show()
                
                self.close()
                
            except ValueError as e:
                print(f"Error al convertir ID_Puesto: {e}")
                QMessageBox.warning(self, "Error", "Error en el tipo de usuario")
        else:
            QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")

    def open_qr_scanner(self):
        if not self.camera:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                QMessageBox.warning(self, "Error", "No se pudo acceder a la cámara")
                return

            # Crear ventana para el escáner QR
            self.scanner_window = QWidget()
            self.scanner_window.setWindowTitle("Escanear QR")
            self.scanner_window.setFixedSize(400, 400)
            
            scanner_layout = QVBoxLayout()
            
            # Label para mostrar el video
            self.camera_label = QLabel()
            self.camera_label.setFixedSize(380, 380)
            scanner_layout.addWidget(self.camera_label)
            
            self.scanner_window.setLayout(scanner_layout)
            self.scanner_window.show()
            
            # Iniciar el timer para actualizar frames
            self.timer.start(30)
        
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Buscar códigos QR en el frame
            qr_codes = decode(frame)
            for qr in qr_codes:
                # Decodificar datos del QR
                data = qr.data.decode('utf-8')
                try:
                    # El formato esperado es "usuario:contraseña"
                    usuario, contraseña = data.split(':')
                    self.timer.stop()
                    self.camera.release()
                    self.scanner_window.close()
                    self.camera = None
                    # Intentar login con las credenciales del QR
                    self.do_login(usuario, contraseña)
                    return
                except:
                    continue

            # Convertir frame de OpenCV a QPixmap
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.camera_label.setPixmap(pixmap.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio))

    def do_login(self, usuario, contraseña):
        resultado = verificar_credenciales(usuario, contraseña)
        if resultado and len(resultado) == 3:
            id_usuario, nombre, id_puesto = resultado
            
            # Set the current user name in globals
            set_current_user(nombre)
            
            try:
                id_puesto = int(id_puesto)
                if id_puesto == 1:
                    self.main_window = p_inicio.MainWindow()
                    self.main_window.show()
                else:
                    self.main_window = Caja.CajaI()
                    self.main_window.show()
                self.close()
            except ValueError as e:
                print(f"Error al convertir ID_Puesto: {e}")
                QMessageBox.warning(self, "Error", "Error en el tipo de usuario")
        else:
            QMessageBox.warning(self, "Acceso denegado", "Código QR inválido")

    def closeEvent(self, event):
        if self.camera:
            self.timer.stop()
            self.camera.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

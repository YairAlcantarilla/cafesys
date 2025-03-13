import p_inicio
import sys
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QGraphicsOpacityEffect
#################################### Interfaz principal de personal #######################################################

class MainPersonal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Mpersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)


        button_configs = [
            ["Caja", 30, 152, 200, 50],
            #otrosbotones
            ["AgregarE", 184, 144, 344, 55],
            ["EliminarE", 184, 225, 344, 55],
            ["EditarE", 184, 306, 344, 55],
            ["ListaE", 184, 387, 344, 55],
            ["RegresarE", 1270, 655, 77, 70],
            
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0);
                    border: 0px solid white;
                    border-radius: 10px;
                    color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 80);
            }
        """)
            self.buttons.append(button)
        
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        button = self.sender()
        if button.text() == "AgregarE":
            self.cambioP = AgregarE()
        elif button.text() == "EliminarE":
            self.cambioP = EliminarE()
        elif button.text() == "Editar":
            self.main_window = EditarProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "ListaE":
            self.main_window = ListaProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "RegresarE":
            self.cambioP = p_inicio.MainWindow()  

        self.fade_out()  
        
    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150) 
        self.animation.setStartValue(1.0)  
        self.animation.setEndValue(0.0)  
        self.animation.finished.connect(self.open_new_window) 
        self.animation.start()

    def open_new_window(self):
        self.cambioP.setWindowOpacity(0.0)  
        self.cambioP.show()
        self.new_animation = QPropertyAnimation(self.cambioP, b"windowOpacity")
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()
       

#################################### Interfaz para agregar empleado #######################################################
class AgregarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Apersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [
            [".", 598, 194, 317, 40],
            [".", 598, 284, 317, 40],
            [".", 598, 369, 317, 40],
           
            [".", 964, 194, 250, 40],
            [".", 964, 284, 250, 40],   
        ]

        self.inputs = []
        for placeholder, x, y, width, height in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)  
            input_field.setFixedSize(width, height)
            input_field.move(x, y)
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #E6AA68;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 14px;
                    background-color: #111A2D;
                    color: #E6AA68;
                }
            """)
            self.inputs.append(input_field)
        
        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
            ["Confirmar", 810, 554, 227, 78],
        ]
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0);
                    border: 0px solid white;
                    border-radius: 10px;
                    color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 80);
            }
        """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
            
        
    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150) 
        self.animation.setStartValue(1.0)  
        self.animation.setEndValue(0.0)  
        self.animation.finished.connect(self.open_new_window) 
        self.animation.start()

    def open_new_window(self):
        self.cambioP.setWindowOpacity(0.0)  
        self.cambioP.show()
        self.new_animation = QPropertyAnimation(self.cambioP, b"windowOpacity")
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()

    
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()     
        elif button.text() == "Confirmar":
            self.cambioP = MainPersonal() 
        self.fade_out()

#################################### Interfaz para eliminar empleado #######################################################
class EliminarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliminar usuario")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Epersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        #**************************************************************
        input_configs = [
            ["Ingrese ID", 598, 194, 317, 40, False],  # ID (Editable)
            ["", 598, 284, 317, 40, True],  # Nombre (Solo lectura)
            ["", 598, 369, 317, 40, True],  # Ocupación (Solo lectura)
        ]

        # 🔹 Lista para almacenar los QLineEdit
        self.inputs = []

        for placeholder, x, y, width, height, read_only in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)
            input_field.setFixedSize(width, height)
            input_field.move(x, y)
            input_field.setReadOnly(read_only)  # Solo lectura si es True

            # 🔹 Estilo visual
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #E6AA68;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 14px;
                    background-color: #111A2D;
                    color: #E6AA68;
                }
                QLineEdit:read-only {
                    background-color: #222A3D;
                    color: #B4B4B4;
                    border: 1px solid #E6AA68;
                }
            """)

            self.inputs.append(input_field)


#**********************************************************************
        button_configs = [
            ["EliminarE", 184, 144, 344, 55],
            ["Confirmar", 810, 554, 227, 78],
            ["Regresar", 1270, 655, 77, 70],
            
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0);
                    border: 0px solid white;
                    border-radius: 10px;
                    color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 80);
            }
        """)
            self.buttons.append(button)
        
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()
        elif button.text() == "Eliminar":
            self.cambioP = MainPersonal()
    
        self.fade_out()  
        
    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150) 
        self.animation.setStartValue(1.0)  
        self.animation.setEndValue(0.0)  
        self.animation.finished.connect(self.open_new_window) 
        self.animation.start()

    def open_new_window(self):
        self.cambioP.setWindowOpacity(0.0)  
        self.cambioP.show()
        self.new_animation = QPropertyAnimation(self.cambioP, b"windowOpacity")
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()
    #***********************************************************************************

#################################### Interfaz para eliminar empleado #######################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPersonal()
    window.show()
    sys.exit(app.exec())
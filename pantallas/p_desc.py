import sys
import p_inicio
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
#####################################################
class MainDesc(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/menu_d.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #boton
        button_configs = [
            ["AgregarD", 273, 144, 343, 55],
            ["EliminarD", 273, 225, 343, 55],
            ["EditarD", 273, 306, 343, 55],
            ["ListaD", 273, 387, 343, 55],
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
            self.main_window = main_p.MainPWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "AgregarD":
            self.main_window = AgregarDto()
            self.main_window.show()
            self.close()
        elif button.text() == "EditarD":
            self.main_window = EditarDto()
            self.main_window.show()
            self.close()
        elif button.text() == "ListaD":
            self.main_window = ListaDto()
            self.main_window.show()
            self.close()
        elif button.text() == "EliminarD":
            self.main_window = EditarDto()
            self.main_window.show()
            self.close()
#################################################
class AgregarDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/AgregarD.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #casillas
        input_configs = [
            [".", 588, 194, 240, 40],
            [".", 588, 281, 240, 40],
            [".", 952, 194, 240, 40],
            [".", 952, 281, 240, 40],
   
        ]

        self.inputs = []
        for placeholder, x, y, width, height in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)  # Texto de referencia dentro del campo
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
            ["Confirmar", 798, 554, 227, 78],
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
            self.main_window = MainDesc()  
            self.main_window.show()
            self.close() 
######################################################################################################
class EliminarDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EliminarDto.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        #cajas
        input_configs = [
            [".", 598, 194, 317, 40],
            [".", 598, 284, 317, 40],   
        ]
        
        self.inputs = []
        for placeholder, x, y, width, height in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)  # Texto de referencia dentro del campo
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
        
        #mais botones
        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
            ["Confirmar", 798, 554, 227, 78],
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
            self.main_window = MainDesc()  
            self.main_window.show()
            self.close() 
######################################################################################################
class EditarDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EditarD.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)


        input_configs = [
            [".", 588, 194, 240, 40],
            [".", 588, 281, 240, 40],
            [".", 952, 194, 240, 40],
            [".", 952, 281, 240, 40],
   
        ]

        self.inputs = []
        for placeholder, x, y, width, height in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)  # Texto de referencia dentro del campo
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
            ["Confirmar", 798, 554, 227, 78],
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
            self.main_window = MainDesc()  
            self.main_window.show()
            self.close()
#####################################################################################################
class ListaDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ListaD.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        button_configs = [
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
            self.main_window = MainDesc()  
            self.main_window.show()
            self.close() 




















#################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDesc()
    window.show()
    sys.exit(app.exec())
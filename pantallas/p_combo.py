import sys
import p_inicio
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
#####################################################
class MainCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/menu_combo.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #boton
        button_configs = [
            ["AgregarC", 273, 144, 343, 55],
            ["EliminarC", 273, 225, 343, 55],
            ["EditarC", 273, 306, 343, 55],
            ["ListaC", 273, 387, 343, 55],
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
                    background-color: rgba(255, 255, 255, 40);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 60);
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
        elif button.text() == "AgregarC":
            self.main_window = AgregarCombo()
            self.main_window.show()
            self.close()
        elif button.text() == "EliminarC":
            self.main_window = EliminarCombo()
            self.main_window.show()
            self.close()
        elif button.text() == "EditarC":
            self.main_window = Editarcombo()
            self.main_window.show()
            self.close()
        elif button.text() == "ListaC":
            self.main_window = Listacombo()
            self.main_window.show()
            self.close()
######################################
class AgregarCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/agregar combo.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        
        
        input_configs = [
            [".", 593, 196, 321, 38],
            [".", 593, 276, 321, 38],
            [".", 593, 360, 321, 38],
            [".", 593, 454, 321, 38],
            [".", 944, 198, 237, 38],
               
        ]

        self.inputs = []
        for placeholder, x, y, width, height in input_configs:
            input_field = QLineEdit(self)
            input_field.setPlaceholderText(placeholder)  # Texto de referencia dentro del campo
            input_field.setFixedSize(width, height)
            input_field.move(x, y)
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 2px solid gray;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 14px;
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
                    background-color: rgba(255, 255, 255, 40);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 60);
                }
            """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainCombo()  
            self.main_window.show()
            self.close() 
 ###########################################################################################       
class EliminarCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Eliminar combo.png')
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
                    border: 2px solid gray;
                    border-radius: 10px;
                    padding: 5px;
                    font-size: 14px;
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
                    background-color: rgba(255, 255, 255, 40);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 60);
                }
            """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)


    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainCombo()  
            self.main_window.show()
            self.close() 


################################################################################################################
class Editarcombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Editar combo.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        
        #boton
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
                    background-color: rgba(255, 255, 255, 40);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 60);
                }
            """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainCombo()  
            self.main_window.show()
            self.close() 
################################################################################################################
class Listacombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo 
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Lista combos.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #BOTON
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
                    background-color: rgba(255, 255, 255, 40);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 60);
                }
            """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainCombo()  
            self.main_window.show()
            self.close() 



 #########

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainCombo()
    window.show()
    sys.exit(app.exec())
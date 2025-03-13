import sys
import p_inicio
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
####################################################################################################
####
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation
#####
####################################################################################################
class MainCaja(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/CajaP.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        button_configs = [
            ["Caja", 278, 165, 290, 440],
            ["productos", 798, 165, 290, 440],
            
            ["Regresar", 1270, 675, 65, 70],
            
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
    #*************************************************************************
    def button_clicked(self):
            button = self.sender()
            
            if button.text() == "Regresar":
                self.cambioP = p_inicio.MainWindow()
            elif button.text() == "Caja":
                from Caja import CajaI 
                self.cambioP = CajaI()
            else:
                return

            self.fade_out()  
    #*************************************************************************

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
        self.new_animation.setDuration(60)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()

    



###############################################################################################
class CajaI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caja")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Caja1.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [
            [".", 694, 161, 285, 38],
            [".", 694, 258, 285, 38],
            [".", 1060, 161, 279, 38],
   
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
            ["Aproducto", 970, 365, 117, 120],
            ["Eproducto", 1163, 365, 117, 120],
            ["Ccompra", 970, 520, 117, 120],
            ["Ecompra", 1163, 520, 117, 120],
            ["Regresar", 1280, 25, 50, 50],
            ["Buscar", 1210, 25, 50, 50],
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
                background-color: rgba(255, 255, 255, );
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
            self.cambioP = p_inicio.MainWindow()  
        elif button.text() == "Buscar":
            self.cambioP = MainCaja()  
        elif button.text() == "Ccompra":
            self.cambioP = CajaFinal()  
        elif button.text() == "Ecompra":
            self.cambioP = MainCaja()  
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
        self.new_animation.setDuration(60)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()
       


###############################################################################################
class CajaFinal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finalizar pedido")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/CajaF.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [     
            [".", 694, 258, 285, 38],
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
            ["Regresar", 1280, 25, 50, 50],
            ["Buscar", 1210, 25, 50, 50],
            ["RegresarA", 1293, 690, 57, 60],
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
                background-color: rgba(255, 255, 255,0);
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
            self.main_window = p_inicio.MainWindow()  
            self.main_window.show()
            
            self.close() 
        elif button.text() == "RegresarA":
            self.main_window = MainCaja()  
            self.main_window.show()
            self.close()   
    

##############
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainCaja()
    window.show()
    sys.exit(app.exec())

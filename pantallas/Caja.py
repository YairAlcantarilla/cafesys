import sys
import login
import p_inicio
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QMessageBox, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,  QDialog)
####################################################################################################
####
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation
#####

###############################################################################################
class CajaI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caja")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Caja1 (2).png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [
            ["Fecha", 825, 305, 150, 38],
            ["Cantidad", 825, 365, 150, 38],
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
            ["Bebida", 710, 126, 132, 132],
            ["Comida", 851, 126, 132, 132],
            ["Combos", 993, 126, 132, 132],
            ["Regresar", 1280, 25, 50, 50],
            ["PEfectivo", 914, 505, 77, 75],
            ["PTarjeta", 1015, 505, 77, 75],
            ["Ayuda", 1210, 25, 50, 50],
        ]
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 50);
                    border: 0px solid white;
                    border-radius: 10px;
                    color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 80);
            }
        """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

        ######################  Tabla de contenido  ####################################################
        self.table = QTableWidget(self)
        self.table.setGeometry(40, 125, 618, 605)  # x, y, width, height
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Producto', 'Fecha', 'Cantidad'])
        
        # Configurar el estilo de la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
            }
            QHeaderView::section {
                background-color: #111A2D;
                color: #E6AA68;
                border: 1px solid #E6AA68;
                padding: 5px;
            }
            QTableWidget::item {
                border: 1px solid #E6AA68;
                padding: 5px;
            }
        """)

        # Ajustar el ancho de las columnas
        header = self.table.horizontalHeader()
        for column in range(3):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

        # Método para agregar una nueva fila
        def agregar_fila(self):
            producto = self.nombre_combo.currentText()
            fecha = self.inputs[0].text()  # El campo de fecha
            cantidad = self.inputs[1].text()  # El campo de cantidad
            
            if producto and fecha and cantidad:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(producto))
                self.table.setItem(row_position, 1, QTableWidgetItem(fecha))
                self.table.setItem(row_position, 2, QTableWidgetItem(cantidad))

        # Conectar el botón "Aproducto" para agregar filas
        for button in self.buttons:
            if button.text() == "Aproducto":
                button.clicked.disconnect()  # Desconectar conexiones previas
                button.clicked.connect(lambda: agregar_fila(self))
    ######################  Tabla de contenido  ####################################################

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.cambioP = login.LoginWindow()  
        elif button.text() == "Buscar":
            pass  
        elif button.text() == "Ccompra":
            self.cambioP = CajaFinal()  
        elif button.text() == "PEfectivo":
            
            self.pago_efectivo_window = PagoEfectivoWindow(self)
            self.pago_efectivo_window.show()
            return  

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
       
    def limpiar_tabla(self):
        self.table.setRowCount(0)

###############################################################################################
class PagoEfectivoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pago en Efectivo")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #192745;")
        
        # Configurar para que sea una ventana flotante
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)

#########################################################################################################
class CajaFinal(QMainWindow):
    pass
##############
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CajaI()
    window.show()
    sys.exit(app.exec())

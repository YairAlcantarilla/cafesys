import sys
import p_inicio
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox
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
##########################################################################################
class AgregarCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ADDC.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Campos de entrada
        self.nombre_combo = QLineEdit(self)
        self.nombre_combo.setPlaceholderText("Nombre del combo")
        self.nombre_combo.setFixedSize(321, 38)
        self.nombre_combo.move(593, 196)
        self.nombre_combo.setStyleSheet(self.estilo_line_edit())
        
        self.precio_combo = QLineEdit(self)
        self.precio_combo.setPlaceholderText("Precio del combo")
        self.precio_combo.setFixedSize(321, 38)
        self.precio_combo.move(593, 451)
        self.precio_combo.setStyleSheet(self.estilo_line_edit())


        # ComboBox para productos
        self.producto1_combo = QComboBox(self)
        self.producto1_combo.setFixedSize(321, 38)
        self.producto1_combo.move(593, 276)
        self.producto1_combo.setStyleSheet(self.estilo_combo_box())

        self.producto2_combo = QComboBox(self)
        self.producto2_combo.setFixedSize(321, 38)
        self.producto2_combo.move(593, 360)
        self.producto2_combo.setStyleSheet(self.estilo_combo_box())

        self.cargar_productos()

        # Botones
        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
            ["Confirmar", 798, 554, 227, 78],
        ]
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet(self.estilo_boton())
            self.buttons.append(button)
            button.clicked.connect(self.button_clicked)

    def estilo_line_edit(self):
        return """
            QLineEdit {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #111A2D;
                color: #E6AA68;
            }
        """

    def estilo_combo_box(self):
        return """
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #111A2D;
                color: #E6AA68;
            }
            QComboBox::drop-down { border: none; }
            QComboBox::down-arrow { image: none; }
            QComboBox QAbstractItemView {
                background-color: #111A2D;
                color: #E6AA68;
                selection-background-color: #E6AA68;
                selection-color: #111A2D;
            }
        """

    def estilo_boton(self):
        return """
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
        """

    def cargar_productos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            for producto in productos:
                self.producto1_combo.addItem(producto[1])
                self.producto2_combo.addItem(producto[1])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainCombo()
            self.main_window.show()
            self.close()
        elif button.text() == "Confirmar":
            self.confirmar_combo()

    def confirmar_combo(self):
        nombre_combo = self.nombre_combo.text()
        producto1 = self.producto1_combo.currentText()
        producto2 = self.producto2_combo.currentText()

        if not nombre_combo or producto1 == producto2:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un nombre válido y seleccione productos distintos.")
            return

        try:
            from conexion import agregar_combo
            agregar_combo(nombre_combo, producto1, producto2)
            QMessageBox.information(self, "Éxito", "Combo agregado correctamente.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar combo: {str(e)}")

 ###########################################################################################

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
            self.main_window = MainCombo()  
            self.main_window.show()
            self.close() 



 #########

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainCombo()
    window.show()
    sys.exit(app.exec())
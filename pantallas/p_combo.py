import sys
import p_inicio
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QComboBox, QMessageBox, 
    QTableWidget, QHeaderView, QTableWidgetItem, QLineEdit
)
from PyQt6.QtGui import QPixmap
from conexion import eliminar_combo, mostrar_combos

#####################################################
class MainCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Combos")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/PCOMB.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "Nombre", "Producto 1", "Producto 2", "Precio"
        ])

        # Estilo de la tabla
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
                gridline-color: #E6AA68;
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

        # Ajustar ancho de columnas
        header = self.table_widget.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self.cargar_datos()

        button_configs = [
            ["Agregar Combo", 875, 144, 343, 55],
            ["Eliminar", 875, 225, 343, 55],
            ["Editar", 875, 306, 343, 55],
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
                    color: rgba(255, 255, 255, 0);
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0);
                }
                QPushButton:pressed {
                    background-color: rgba(230, 170, 104, 80);
                }
            """)
            self.buttons.append(button)
            button.clicked.connect(self.button_clicked)

    def cargar_datos(self):
        try:
            from conexion import mostrar_combos
            combos = mostrar_combos()
        
            self.table_widget.setRowCount(len(combos))
        
            for fila, combo in enumerate(combos):
                # combo[0] = Nombre del combo
                # combo[1] = Nombre del producto 1
                # combo[2] = Nombre del producto 2
                # combo[3] = Precio
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(combo[0])))  # Nombre del combo
                self.table_widget.setItem(fila, 1, QTableWidgetItem(str(combo[1])))  # Producto 1
                self.table_widget.setItem(fila, 2, QTableWidgetItem(str(combo[2])))  # Producto 2
                self.table_widget.setItem(fila, 3, QTableWidgetItem(f"${str(combo[3])}"))  # Precio
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los combos: {str(e)}")


    def button_clicked(self):
        button = self.sender()
        if button.text() == "Agregar Combo":
            self.main_window = AgregarCombo()
            self.main_window.show()
        elif button.text() == "Eliminar":
            self.dialog = EliminarCombo()
            self.dialog.show()
        elif button.text() == "Editar":
            self.dialog = Editarcombo()
            self.dialog.show()
        elif button.text() == "Regresar":
            self.main_window = main_p.MainPWindow()  
            self.main_window.show()
            self.close()


##########################################################################################
class AgregarCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(400, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ACOMB.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Campos de entrada
        self.nombre_combo = QLineEdit(self)
        self.nombre_combo.setPlaceholderText("Nombre del combo")
        self.nombre_combo.setFixedSize(321, 38)
        self.nombre_combo.move(30, 120)
        self.nombre_combo.setStyleSheet(self.estilo_line_edit())
        
        self.precio_combo = QLineEdit(self)
        self.precio_combo.setPlaceholderText("Precio del combo")
        self.precio_combo.setFixedSize(321, 38)
        self.precio_combo.move(30, 180)
        self.precio_combo.setStyleSheet(self.estilo_line_edit())

        # ComboBox para productos
        self.producto1_combo = QComboBox(self)
        self.producto1_combo.setFixedSize(321, 38)
        self.producto1_combo.move(30, 230)
        self.producto1_combo.setStyleSheet(self.estilo_combo_box())

        self.producto2_combo = QComboBox(self)
        self.producto2_combo.setFixedSize(321, 38)
        self.producto2_combo.move(30, 280)
        self.producto2_combo.setStyleSheet(self.estilo_combo_box())

        self.cargar_productos()

        # Botones
        button_configs = [
            ["Confirmar", 73, 403, 100, 60],
            ["Regresar", 227, 403, 100, 60],
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
        
        try:
            precio_combo = float(self.precio_combo.text())
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un precio válido.")
            return

        if not nombre_combo or producto1 == producto2:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un nombre válido y seleccione productos distintos.")
            return

        try:
            from conexion import agregar_combo
            agregar_combo(nombre_combo, producto1, producto2, precio_combo)
            QMessageBox.information(self, "Éxito", "Combo agregado correctamente.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar combo: {str(e)}")


###########################################################################################

class EliminarCombo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliminar Combo")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #111A2D;")

        # Crear labels
        label = QLabel("Seleccione combo:", self)
        label.setStyleSheet("color: #E6AA68; font-size: 14px;")
        label.move(30, 30)

        # Crear ComboBox para combos
        self.combo_combo = QComboBox(self)
        self.combo_combo.setFixedSize(200, 30)
        self.combo_combo.move(160, 25)
        self.combo_combo.setStyleSheet("""
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
        """)

        # Cargar combos
        self.cargar_combos()

        # Botones
        button_configs = [
            ["Cancelar", 30, 250, 100, 30],
            ["Eliminar", 270, 250, 100, 30],
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #E6AA68;
                    border-radius: 10px;
                    color: #111A2D;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #D69958;
                }
                QPushButton:pressed {
                    background-color: #C68948;
                }
            """)
            self.buttons.append(button)
            button.clicked.connect(self.button_clicked)

    def cargar_combos(self):
        # Primero agregamos un ítem por defecto
        self.combo_combo.addItem("Seleccionar combo")

        try:
            combos = mostrar_combos()
            # Agregamos solo los nombres de los combos al combo
            for combo in combos:
                self.combo_combo.addItem(combo[0])  # combo[0] es el nombre del combo
        except Exception as e:
            print(f"Error al cargar combos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Eliminar":
            combo_seleccionado = self.combo_combo.currentText()
            if combo_seleccionado != "Seleccionar combo":
                try:
                    eliminar_combo(combo_seleccionado)
                    
                    # Actualizar la ventana principal con los cambios
                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, MainCombo):
                            widget.cargar_datos()
                            break
                    
                    QMessageBox.information(self, "Éxito", "Combo eliminado correctamente")
                    # Reset combo y recargar los combos
                    self.combo_combo.clear()
                    self.cargar_combos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el combo:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un combo")

###########################################################################################       
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
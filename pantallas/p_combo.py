import sys
import p_inicio
import main_p
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QComboBox, QMessageBox, 
    QTableWidget, QHeaderView, QTableWidgetItem, QLineEdit, QTextEdit
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

        self.last_window = None

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
            
            # Debug para ver qué datos estamos recibiendo
            print("Datos recibidos de mostrar_combos:", combos)
            
            if not combos:
                self.table_widget.setRowCount(0)
                return
                
            self.table_widget.setRowCount(len(combos))
        
            for fila, combo in enumerate(combos):
                try:
                    # Asegurarse de que cada columna tenga datos válidos
                    nombre = str(combo[0]) if combo[0] is not None else ""
                    producto1 = str(combo[1]) if combo[1] is not None else ""
                    producto2 = str(combo[2]) if combo[2] is not None else ""
                    precio = f"${str(combo[3])}" if combo[3] is not None else "$0.00"
                    
                    self.table_widget.setItem(fila, 0, QTableWidgetItem(nombre))
                    self.table_widget.setItem(fila, 1, QTableWidgetItem(producto1))
                    self.table_widget.setItem(fila, 2, QTableWidgetItem(producto2))
                    self.table_widget.setItem(fila, 3, QTableWidgetItem(precio))
                except IndexError as e:
                    print(f"Error en el índice del combo {fila}: {e}")
                    print(f"Datos del combo: {combo}")
                    
        except Exception as e:
            print(f"Error detallado al cargar los combos: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar los combos: {str(e)}")

    def actualizar_tabla(self):
        """Actualiza los datos de la tabla"""
        self.cargar_datos()

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Agregar Combo":
            self.last_window = AgregarCombo()
            self.last_window.combo_agregado.connect(self.actualizar_tabla)
            self.last_window.show()
        elif button.text() == "Eliminar":
            self.last_window = EliminarCombo()
            self.last_window.combo_eliminado.connect(self.actualizar_tabla)
            self.last_window.show()
        elif button.text() == "Editar":
            self.last_window = EditarCombo()
            self.last_window.combo_editado.connect(self.actualizar_tabla)
            self.last_window.show()
        elif button.text() == "Regresar":
            self.main_window = main_p.MainPWindow()  
            self.main_window.show()
            self.close()


##########################################################################################
class AgregarCombo(QMainWindow):
    combo_agregado = pyqtSignal()

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
            self.combo_agregado.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar combo: {str(e)}")


###########################################################################################

class EliminarCombo(QMainWindow):
    combo_eliminado = pyqtSignal()

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
                    QMessageBox.information(self, "Éxito", "Combo eliminado correctamente")
                    self.combo_eliminado.emit()
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el combo:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un combo")

###########################################################################################       
################################################################################################################
class EditarCombo(QMainWindow):
    combo_editado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Combo")
        self.setFixedSize(500, 500)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Fondo
        self.background_label = QLabel(self)
        pixmap = QPixmap("imagenes/Editar_combo.png")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        layout.addWidget(self.background_label)

        # ComboBox para seleccionar el combo
        self.combo_selector = QComboBox(self)
        self.combo_selector.setPlaceholderText("Seleccionar combo")
        self.combo_selector.currentIndexChanged.connect(self.cargar_datos_combo)
        self.combo_selector.setGeometry(30, 120, 321, 38)
        self.combo_selector.setStyleSheet(self.estilo_combo_box())

        # Campos de edición
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre del combo")
        self.nombre_input.setGeometry(30, 180, 321, 38)
        self.nombre_input.setStyleSheet(self.estilo_line_edit())
        
        self.producto1_combo = QComboBox(self)
        self.producto1_combo.setGeometry(30, 240, 321, 38)
        self.producto1_combo.setStyleSheet(self.estilo_combo_box())
        
        self.producto2_combo = QComboBox(self)
        self.producto2_combo.setGeometry(30, 300, 321, 38)
        self.producto2_combo.setStyleSheet(self.estilo_combo_box())
        
        self.precio_input = QLineEdit(self)
        self.precio_input.setPlaceholderText("Precio")
        self.precio_input.setGeometry(30, 360, 321, 38)
        self.precio_input.setStyleSheet(self.estilo_line_edit())

        # Botones
        button_configs = [
            ["Guardar", 73, 420, 100, 60],
            ["Cancelar", 227, 420, 100, 60],
        ]
        
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet(self.estilo_boton())
            button.clicked.connect(self.button_clicked)
            self.buttons.append(button)

        # Cargar datos
        self.cargar_combos()
        self.cargar_productos()

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

    def cargar_combos(self):
        """Carga la lista de combos en el ComboBox."""
        try:
            from conexion import mostrar_combos
            combos = mostrar_combos()
            self.combo_selector.addItem("Seleccionar combo")
            for combo in combos:
                self.combo_selector.addItem(combo[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar combos: {str(e)}")

    def cargar_productos(self):
        """Carga la lista de productos en los ComboBoxes."""
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            for producto in productos:
                self.producto1_combo.addItem(producto[1])
                self.producto2_combo.addItem(producto[1])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def cargar_datos_combo(self):
        """Carga los datos del combo seleccionado."""
        nombre_combo = self.combo_selector.currentText()
        if nombre_combo == "Seleccionar combo":
            return
        
        try:
            from conexion import cargar_datos_combo
            combo = cargar_datos_combo(nombre_combo)
            if combo:
                self.nombre_input.setText(combo[0])
                index1 = self.producto1_combo.findText(combo[1])
                index2 = self.producto2_combo.findText(combo[2])
                self.producto1_combo.setCurrentIndex(index1 if index1 >= 0 else 0)
                self.producto2_combo.setCurrentIndex(index2 if index2 >= 0 else 0)
                self.precio_input.setText(str(combo[3]))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del combo: {str(e)}")

    def button_clicked(self):
        """Maneja los eventos de los botones."""
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Guardar":
            self.guardar_cambios()

    def guardar_cambios(self):
        """Guarda los cambios realizados en el combo."""
        if not self.validar_datos():
            return
        
        nombre_combo = self.combo_selector.currentText()
        if nombre_combo == "Seleccionar combo":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un combo para editar")
            return
        
        try:
            datos = {
                "nombre": self.nombre_input.text(),
                "producto1": self.producto1_combo.currentText(),
                "producto2": self.producto2_combo.currentText(),
                "precio": float(self.precio_input.text())
            }
            
            if datos["producto1"] == datos["producto2"]:
                QMessageBox.warning(self, "Advertencia", "Los productos deben ser diferentes")
                return
                
            from conexion import actualizar_combo
            actualizar_combo(nombre_combo, datos)
            QMessageBox.information(self, "Éxito", "Combo actualizado correctamente")
            self.combo_editado.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el combo: {str(e)}")

    def validar_datos(self):
        """Valida que los datos ingresados sean correctos."""
        if not self.nombre_input.text() or not self.precio_input.text():
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos")
            return False
        try:
            float(self.precio_input.text())
            return True
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "El precio debe ser un número válido")
            return False

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
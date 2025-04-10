import sys
sys.path.append("c:/Users/Miriam/Desktop/cafesys")
import p_inicio
import main_p
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QComboBox, QMessageBox, 
    QTableWidget, QHeaderView, QTableWidgetItem, QLineEdit, QTextEdit, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from conexion import eliminar_combo, mostrar_combos, ocultar_combo
from widgets.transfer_list import TransferList

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
        self.table_widget.setColumnCount(3)  # Cambiar a 3 columnas
        self.table_widget.setHorizontalHeaderLabels([
            "Nombre", "Productos", "Precio"  # Cambiar headers
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
        for i in range(3):
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
            
            print("Datos recibidos de mostrar_combos:", combos)
            
            if not combos:
                self.table_widget.setRowCount(0)
                return
                
            self.table_widget.setRowCount(len(combos))
        
            for fila, combo in enumerate(combos):
                try:
                    nombre = str(combo[0]) if combo[0] is not None else ""
                    # Asegurarse de que los productos estén separados correctamente
                    productos = combo[1] if combo[1] else ""
                    precio = f"${str(combo[2])}" if combo[2] is not None else "$0.00"
                    
                    self.table_widget.setItem(fila, 0, QTableWidgetItem(nombre))
                    
                    # Crear item para productos con formato mejorado
                    productos_item = QTableWidgetItem(productos)
                    productos_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                    self.table_widget.setItem(fila, 1, productos_item)
                    
                    self.table_widget.setItem(fila, 2, QTableWidgetItem(precio))
                    
                    # Ajustar altura de la fila según el contenido
                    self.table_widget.resizeRowToContents(fila)
                    
                except IndexError as e:
                    print(f"Error en el índice del combo {fila}: {e}")
                    print(f"Datos del combo: {combo}")
                    
        except Exception as e:
            print(f"Error detallado al cargar los combos: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar los combos: {str(e)}")

        # Ajustar ancho de columnas después de cargar los datos
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Nombre
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Productos
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Precio

        # Ajustar altura de filas para mostrar todo el contenido
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

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
        self.setFixedSize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Campos de entrada
        input_widget = QWidget()
        input_layout = QHBoxLayout()
        
        self.nombre_combo = QLineEdit()
        self.nombre_combo.setPlaceholderText("Nombre del combo")
        self.nombre_combo.setStyleSheet(self.estilo_line_edit())
        
        self.precio_combo = QLineEdit()
        self.precio_combo.setPlaceholderText("Precio del combo")
        self.precio_combo.setStyleSheet(self.estilo_line_edit())
        
        input_layout.addWidget(self.nombre_combo)
        input_layout.addWidget(self.precio_combo)
        input_widget.setLayout(input_layout)
        layout.addWidget(input_widget)

        # Transfer List
        self.transfer_list = TransferList("Productos Disponibles", "Productos en Combo")
        layout.addWidget(self.transfer_list)
        
        # Cargar productos disponibles
        self.cargar_productos()

        # Botones
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        
        confirmar_btn = QPushButton("Confirmar")
        cancelar_btn = QPushButton("Cancelar")
        
        confirmar_btn.setStyleSheet(self.estilo_boton())
        cancelar_btn.setStyleSheet(self.estilo_boton())
        
        button_layout.addWidget(confirmar_btn)
        button_layout.addWidget(cancelar_btn)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        confirmar_btn.clicked.connect(self.confirmar_combo)
        cancelar_btn.clicked.connect(self.close)

    def cargar_productos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            nombres_productos = [producto[1] for producto in productos]
            self.transfer_list.set_available_items(nombres_productos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def confirmar_combo(self):
        nombre_combo = self.nombre_combo.text()
        productos_seleccionados = self.transfer_list.get_selected_items()
        
        try:
            precio_combo = float(self.precio_combo.text())
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un precio válido.")
            return

        if not nombre_combo or len(productos_seleccionados) < 2:
            QMessageBox.warning(self, "Advertencia", 
                              "Por favor ingrese un nombre válido y seleccione al menos dos productos.")
            return

        try:
            from conexion import agregar_combo_multiple
            agregar_combo_multiple(nombre_combo, productos_seleccionados, precio_combo)
            QMessageBox.information(self, "Éxito", "Combo agregado correctamente.")
            self.combo_agregado.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar combo: {str(e)}")

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

    def estilo_boton(self):
        return """
            QPushButton {
                background-color: #E6AA68;
                border-radius: 10px;
                padding: 8px;
                color: #111A2D;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D69958;
            }
            QPushButton:pressed {
                background-color: #C68948;
            }
        """


###########################################################################################

class EliminarCombo(QMainWindow):
    combo_eliminado = pyqtSignal()

    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        # Fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ELIMCOMBO.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        self.setWindowTitle("Eliminar Combo") 
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #111A2D;")

        # Crear labels
        label = QLabel("Seleccione combo:", self)
        label.setStyleSheet("color: #E6AA68; font-size: 14px;")
        label.move(30, 120)

        # Crear ComboBox para combos
        self.combo_combo = QComboBox(self)
        self.combo_combo.setFixedSize(200, 30)
        self.combo_combo.move(160, 120)
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
        self.combo_combo.clear()
        self.combo_combo.addItem("Seleccionar combo")

        try:
            combos = mostrar_combos()  # Esta función ya filtra los combos ocultos
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
                    reply = QMessageBox.question(
                        self,
                        'Confirmación',
                        '¿Está seguro de ocultar este combo?\nNo estará disponible para su uso.',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        ocultar_combo(combo_seleccionado)  # Usar la nueva función
                        QMessageBox.information(self, "Éxito", "Combo ocultado correctamente")
                        self.combo_eliminado.emit()
                        self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo ocultar el combo:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un combo")

###########################################################################################       
################################################################################################################
class EditarCombo(QMainWindow):
    combo_editado = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editar combo")
        self.setFixedSize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Selector de combo
        selector_widget = QWidget()
        selector_layout = QHBoxLayout()
        
        label = QLabel("Seleccione combo:")
        label.setStyleSheet("color: #E6AA68; font-size: 14px;")
        self.combo_selector = QComboBox()
        self.combo_selector.setStyleSheet(self.estilo_combo_box())
        self.combo_selector.currentIndexChanged.connect(self.cargar_datos_combo)
        
        selector_layout.addWidget(label)
        selector_layout.addWidget(self.combo_selector)
        selector_widget.setLayout(selector_layout)
        layout.addWidget(selector_widget)

        # Campos de entrada
        input_widget = QWidget()
        input_layout = QHBoxLayout()
        
        self.nombre_combo = QLineEdit()
        self.nombre_combo.setPlaceholderText("Nombre del combo")
        self.nombre_combo.setStyleSheet(self.estilo_line_edit())
        
        self.precio_combo = QLineEdit()
        self.precio_combo.setPlaceholderText("Precio del combo")
        self.precio_combo.setStyleSheet(self.estilo_line_edit())
        
        input_layout.addWidget(self.nombre_combo)
        input_layout.addWidget(self.precio_combo)
        input_widget.setLayout(input_layout)
        layout.addWidget(input_widget)

        # Transfer List
        self.transfer_list = TransferList("Productos Disponibles", "Productos en Combo")
        layout.addWidget(self.transfer_list)

        # Botones
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        
        guardar_btn = QPushButton("Guardar cambios")
        cancelar_btn = QPushButton("Cancelar")
        
        guardar_btn.setStyleSheet(self.estilo_boton())
        cancelar_btn.setStyleSheet(self.estilo_boton())
        
        button_layout.addWidget(guardar_btn)
        button_layout.addWidget(cancelar_btn)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        guardar_btn.clicked.connect(self.guardar_cambios)
        cancelar_btn.clicked.connect(self.close)

        # Cargar datos iniciales
        self.cargar_combos()
        self.cargar_productos()

    def cargar_combos(self):
        try:
            combos = mostrar_combos()
            self.combo_selector.addItem("Seleccionar combo")
            for combo in combos:
                self.combo_selector.addItem(combo[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar combos: {str(e)}")

    def cargar_productos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            nombres_productos = [producto[1] for producto in productos]
            self.transfer_list.set_available_items(nombres_productos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def cargar_datos_combo(self):
        nombre_combo = self.combo_selector.currentText()
        if nombre_combo == "Seleccionar combo":
            self.nombre_combo.clear()
            self.precio_combo.clear()
            self.transfer_list.set_selected_items([])
            return
        
        try:
            from conexion import cargar_datos_combo
            combo = cargar_datos_combo(nombre_combo)
            if combo:
                self.nombre_combo.setText(combo[0])
                # Los productos vienen como string separado por comas, convertirlos a lista
                productos = [p.strip() for p in combo[1].split(',') if p.strip()]
                self.precio_combo.setText(str(combo[2]))
                
                # Actualizar la lista de productos seleccionados
                self.transfer_list.set_selected_items(productos)
                
                # Mover los productos seleccionados de la lista disponible
                for producto in productos:
                    items = self.transfer_list.left_list.findItems(producto, Qt.MatchFlag.MatchExactly)
                    for item in items:
                        self.transfer_list.left_list.takeItem(self.transfer_list.left_list.row(item))
        except Exception as e:
            print(f"Error al cargar datos del combo: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos del combo: {str(e)}")

    def guardar_cambios(self):
        nombre_original = self.combo_selector.currentText()
        if nombre_original == "Seleccionar combo":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un combo para editar")
            return
        
        try:
            nombre_nuevo = self.nombre_combo.text()
            productos_seleccionados = self.transfer_list.get_selected_items()
            precio = float(self.precio_combo.text())
            
            if not nombre_nuevo or len(productos_seleccionados) < 2:
                QMessageBox.warning(self, "Advertencia", 
                                "Por favor ingrese un nombre válido y seleccione al menos dos productos.")
                return

            from conexion import actualizar_combo_multiple
            actualizar_combo_multiple(nombre_original, nombre_nuevo, productos_seleccionados, precio)
            QMessageBox.information(self, "Éxito", "Combo actualizado correctamente")
            self.combo_editado.emit()
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un precio válido")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el combo: {str(e)}")

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
                background-color: #E6AA68;
                border-radius: 10px;
                padding: 8px;
                color: #111A2D;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D69958;
            }
            QPushButton:pressed {
                background-color: #C68948;
            }
        """

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
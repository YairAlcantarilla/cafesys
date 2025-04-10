import sys
import Caja, P_Registros, personal, login, p_inventario
import p_inicio
import conexion
import main_p
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QMessageBox, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,QMessageBox) 
####################################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/menu_producto.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)  # x, y, width, height
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "Nombre", "Categoría", "Stock", "Precio"
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

        # Ajustar el ancho de las columnas
        header = self.table_widget.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Cargar datos
        self.cargar_datos()

        button_configs = [
            #Botones laterales
            ["Caja", 30, 152, 60, 50],
            ["Reportes", 30, 227, 60, 50],
            ["Productos", 30, 303, 60, 50],
            ["Personal", 30, 378, 60, 50],
            ["Inventario", 30, 454, 60, 50],
            ["Ajustes", 30, 530, 60, 50],
            ["Salir", 30, 605, 60, 50],
            #otrosbotones
            ["Agregar Producto", 875, 144, 343, 55],
            ["Eliminar", 875, 225, 343, 55],
            ["Editar", 875, 306, 343, 55],
            ["Recargar", 875, 387, 343, 55],  # Nuevo botón de recarga
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
                    color:  rgba(255, 255, 255, 0);
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

    def cargar_datos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos(ocultar_especiales=True)
            
            self.table_widget.setRowCount(len(productos))
            
            for fila, producto in enumerate(productos):
                # producto[1] = Nombre
                # producto[2] = Precio
                # producto[3] = Stock/Cantidad
                # producto[4] = Categoría
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(producto[1])))  # Nombre
                self.table_widget.setItem(fila, 2, QTableWidgetItem(str(producto[4])))  # Categoría
                self.table_widget.setItem(fila, 1, QTableWidgetItem(str(producto[3])))  # Stock/Cantidad
                self.table_widget.setItem(fila, 3, QTableWidgetItem(f"${str(producto[2])}"))  # Precio

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(f"Error al cargar los productos: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Agregar Producto":
            self.main_window = AgregarProducto()
            self.main_window.producto_agregado.connect(self.cargar_datos)  # Nueva conexión
            self.main_window.show()
        elif button.text() == "Eliminar":
            self.dialog = EliminarProducto()
            self.dialog.producto_eliminado.connect(self.cargar_datos)  # Nueva conexión
            self.dialog.show()
        elif button.text() == "Editar":
            self.dialog = EditarProducto()
            self.dialog.producto_editado.connect(self.cargar_datos)  # Nueva conexión
            self.dialog.show()
        elif button.text() == "Recargar":  # Nuevo handler
            self.cargar_datos()
            QMessageBox.information(self, "Éxito", "Datos actualizados correctamente")
        elif button.text() == "Lista":
            self.main_window = ListaProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "Regresar":
            self.main_window = main_p.MainPWindow()  
            self.main_window.show()
            self.close()
        elif button.text() == "Caja":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de producto?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = Caja.CajaI()
                self.main_window.show()
                self.close()

        elif button.text() == "Reportes":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de producto?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = P_Registros.MainR()
                self.main_window.show()
                self.close()


        elif button.text() == "Productos":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de producto?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = main_p.MainPWindow()
                self.main_window.show()
                self.close()
        
        elif button.text() == "Personal":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de producto?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = personal.MainPersonal()
                self.main_window.show()
                self.close()
        elif button.text() == "Inventario":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de producto?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = p_inventario.MainWindow()
                self.main_window.show()
                self.close()
        
        elif button.text() == "Salir":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de salir a la pantalla principal?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = login.LoginWindow()
                self.main_window.show()
                self.close()


########################################################################################################
class AgregarProducto(QMainWindow):
    producto_agregado = pyqtSignal()  # Nueva señal

    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        # Fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/PAP.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
    
        self.setWindowTitle("Agregar Producto")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #111A2D;")

        # Crear labels
        labels = ["Nombre:", "Precio:", "Stock:", "Categoría:"]
        self.label_widgets = []
        
        for i, text in enumerate(labels):
            label = QLabel(text, self)
            label.setStyleSheet("color: #E6AA68; font-size: 14px;")
            label.move(30, 152 + i * 60)
            self.label_widgets.append(label)

        # Crear inputs
        self.inputs = []
        for i in range(3):  # Solo 3 inputs (nombre, precio, stock)
            input_field = QLineEdit(self)
            input_field.setFixedSize(200, 30)
            input_field.move(160, 150 + i * 60)
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

        # Crear ComboBox para categorías
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.setFixedSize(200, 30)
        self.categoria_combo.move(160, 325)
        self.categoria_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #111A2D;
                color: #E6AA68;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                background-color: #111A2D;
                color: #E6AA68;
                selection-background-color: #E6AA68;
                selection-color: #111A2D;
            }
        """)
        
        # Cargar categorías desde la BD
        self.cargar_categorias()

        # Botones
        button_configs = [
            ["Cancelar", 30, 400, 100, 30],
            ["Guardar", 270, 400, 100, 30],
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

    def cargar_categorias(self):
        try:
            from conexion import obtener_categorias
            categorias = obtener_categorias()
            self.categoria_combo.addItem("Seleccionar categoría")
            for categoria in categorias:
                self.categoria_combo.addItem(categoria[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar categorías: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Guardar":
            if self.validar_datos():
                self.guardar_producto()

    def validar_datos(self):
        if not all(input.text() for input in self.inputs):
            QMessageBox.warning(self, "Advertencia", "Por favor complete todos los campos")
            return False
        if self.categoria_combo.currentText() == "Seleccionar categoría":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una categoría")
            return False
        try:
            float(self.inputs[1].text())  # Validar precio
            int(self.inputs[2].text())    # Validar stock
            return True
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Precio y stock deben ser números válidos")
            return False

    def guardar_producto(self):
        try:
            # Get the next available ID
            from conexion import get_next_id
            next_id = get_next_id("Producto", "ID_Producto")
            
            datos = {
                "ID_Producto": next_id,
                "Nombre": self.inputs[0].text(),
                "Precio": float(self.inputs[1].text()),
                "Categoria": self.categoria_combo.currentText(),
                "Cantidad": int(self.inputs[2].text())
            }
            conexion.insertar_dato("Producto", datos)
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
            self.producto_agregado.emit()  # Emitir señal
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el producto:\n{str(e)}")

######################################################################################################
class EliminarProducto(QMainWindow):
    producto_eliminado = pyqtSignal()  # Nueva señal

    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ELIMP.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        self.setWindowTitle("Eliminar Producto")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #000928;")

        # Crear labels
        label = QLabel("Producto:", self)
        label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        label.move(30, 152)

        # Crear ComboBox para productos 
        self.producto_combo = QComboBox(self)
        self.producto_combo.setFixedSize(200, 30)
        self.producto_combo.move(160, 150)
        self.producto_combo.setStyleSheet("""
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

        # Cargar productos
        self.cargar_productos()

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

    def cargar_productos(self):
        # Primero agregamos un ítem por defecto
        self.producto_combo.addItem("Seleccionar producto")
        
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos(ocultar_especiales=True)
            # Agregamos solo los nombres de los productos al combo
            for producto in productos:
                self.producto_combo.addItem(producto[1])  # producto[1] es el nombre
        except Exception as e:
            print(f"Error al cargar productos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Eliminar":
            producto_seleccionado = self.producto_combo.currentText()
            if producto_seleccionado != "Seleccionar producto":
                try:
                    from conexion import eliminar_producto
                    eliminar_producto(producto_seleccionado)

                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, MainWindow):
                            widget.cargar_datos()
                            break
                    
                    QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                    self.producto_eliminado.emit()  # Emitir señal
                    self.producto_combo.clear()
                    self.cargar_productos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un producto")

##########################################################################################################
class EditarProducto(QMainWindow):
    producto_editado = pyqtSignal()  # Nueva señal

    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EDITP.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        self.setWindowTitle("Editar Producto")
        self.setFixedSize(400, 520)
        self.setStyleSheet("background-color: #111A2D;")

        # Crear labels
        labels = ["Producto:", "Nombre:", "Precio:", "Stock:", "Categoría:"]
        self.label_widgets = []
        
        for i, text in enumerate(labels):
            label = QLabel(text, self)
            label.setStyleSheet("color: #E6AA68; font-size: 14px;")
            label.move(30, 125 + i * 60)
            self.label_widgets.append(label)

        # Crear ComboBox para seleccionar producto
        self.producto_combo = QComboBox(self)
        self.producto_combo.setFixedSize(200, 30)
        self.producto_combo.move(160, 120)
        self.producto_combo.setStyleSheet("""
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
        self.producto_combo.currentIndexChanged.connect(self.cargar_datos_producto)

        # Crear inputs
        self.inputs = []
        for i in range(3):
            input_field = QLineEdit(self)
            input_field.setFixedSize(200, 30)
            input_field.move(160, 190 + i * 60)
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

        # Crear ComboBox para categorías
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.setFixedSize(200, 30)
        self.categoria_combo.move(160, 365)
        self.categoria_combo.setStyleSheet(self.producto_combo.styleSheet())

        # Cargar datos
        self.cargar_productos()
        self.cargar_categorias()

        # Botones
        button_configs = [
            ["Cancelar", 30, 450, 100, 30],
            ["Guardar", 270, 450, 100, 30],
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

    def cargar_productos(self):
        self.producto_combo.addItem("Seleccionar producto")
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos(ocultar_especiales=True)
            for producto in productos:
                self.producto_combo.addItem(producto[1])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def cargar_categorias(self):
        try:
            from conexion import obtener_categorias
            categorias = obtener_categorias()
            self.categoria_combo.addItem("Seleccionar categoría")
            for categoria in categorias:
                self.categoria_combo.addItem(categoria[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar categorías: {str(e)}")

    def cargar_datos_producto(self):
        if self.producto_combo.currentText() != "Seleccionar producto":
            try:
                from conexion import obtener_producto_por_nombre
                producto = obtener_producto_por_nombre(self.producto_combo.currentText())
                if producto:
                    # producto[0] = ID_producto
                    # producto[1] = nombre
                    # producto[2] = precio 
                    # producto[3] = cantidad/stock
                    # producto[4] = categoria
                    
                    self.inputs[0].setText(str(producto[1]))     # Nombre
                    self.inputs[1].setText(str(producto[2]))     # Precio
                    self.inputs[2].setText(str(producto[4]))     # Stock/Cantidad
                    
                    # Seleccionar la categoría correcta
                    categoria = str(producto[4])
                    index = self.categoria_combo.findText(categoria)
                    if index >= 0:
                        self.categoria_combo.setCurrentIndex(index)
                    else:
                        self.categoria_combo.setCurrentIndex(0)
                        
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar datos del producto: {str(e)}")

    def validar_datos(self):
        if not all(input.text() for input in self.inputs):
            QMessageBox.warning(self, "Advertencia", "Por favor complete todos los campos")
            return False
        if self.categoria_combo.currentText() == "Seleccionar categoría":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione una categoría")
            return False
        try:
            float(self.inputs[1].text())  # Validar precio
            int(self.inputs[2].text())    # Validar stock
            return True
        except ValueError:
            QMessageBox.warning(self, "Advertencia", "Precio y stock deben ser números válidos")
            return False

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Guardar":
            if self.validar_datos():
                self.guardar_cambios()

    def guardar_cambios(self):
        try:
            datos = {
                "Nombre": self.inputs[0].text(),
                "Precio": float(self.inputs[1].text()),
                "Cantidad": int(self.inputs[2].text()),
                "Categoria": self.categoria_combo.currentText() 
            }
            from conexion import actualizar_producto
            actualizar_producto(self.producto_combo.currentText(), datos)
            
            # Actualizar la ventana principal
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, MainWindow):
                    widget.cargar_datos()
                    break
                    
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente")
            self.producto_editado.emit()  # Emitir señal
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el producto:\n{str(e)}")

##############################################################################    

class ListaProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista de Productos")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/listadp.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(278, 165, 850, 450)  # x, y, width, height
        self.table_widget.setColumnCount(4)  # 4 columnas
        self.table_widget.setHorizontalHeaderLabels([
            "Nombre", "Precio", "Stock", "Categoria"
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

        # Ajustar el ancho de las columnas
        header = self.table_widget.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Cargar datos
        self.cargar_datos()

        # Botón Regresar
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

    def cargar_datos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos(ocultar_especiales=True)
            
            self.table_widget.setRowCount(len(productos))
            
            for fila, producto in enumerate(productos):
                # Asumiendo que producto[1] es nombre, producto[2] es categoría,
                # producto[3] es stock y producto[4] es precio
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(producto[1])))
                self.table_widget.setItem(fila, 1, QTableWidgetItem(str(producto[2])))
                self.table_widget.setItem(fila, 2, QTableWidgetItem(str(producto[3])))
                self.table_widget.setItem(fila, 3, QTableWidgetItem(f"${str(producto[4])}"))
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(f"Error al cargar los productos: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

#############################################################################




#############################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

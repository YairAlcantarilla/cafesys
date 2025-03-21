import sys
import p_inicio
import conexion
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QMessageBox, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
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
        pixmap = QPixmap('imagenes/inventario.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(355, 131, 690, 555)  # x, y, width, height
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoria", "Stock"
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
            ["Caja", 30, 152, 200, 50],
            ["Reportes", 30, 227, 200, 50],
            ["Productos", 30, 303, 200, 50],
            ["Personal", 30, 378, 200, 50],
            ["Inventario", 30, 454, 200, 50],
            ["Ajustes", 30, 530, 200, 50],
            ["Salir", 30, 605, 200, 50],
            #otrosbotones
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
                background-color: rgba(230, 170, 104, 0);
            }
        """)
            self.buttons.append(button)
        
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def cargar_datos(self):
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            
            self.table_widget.setRowCount(len(productos))
            
            for fila, producto in enumerate(productos):
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
        if button.text() == "Agregar Producto":
            self.main_window = AgregarProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "Eliminar":
            self.main_window = EliminarProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "Editar":
            self.main_window = EditarProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "Lista":
            self.main_window = ListaProducto()
            self.main_window.show()
            self.close()
        elif button.text() == "Regresar":
            self.main_window = main_p.MainPWindow()  
            self.main_window.show()
            self.close()
########################################################################################################
class AgregarProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Producto")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/agregarpr.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        
        input_configs = [
            ["Nombre", 598, 194, 317, 40],
            ["Categoria", 598, 284, 317, 40],
            ["3", 598, 374, 317, 40],
            ["4", 994, 198, 250, 40],
             
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
            self.main_window = MainWindow()  
            self.main_window.show()
            self.close()   
        elif button.text() == "Confirmar":
            datos = {
                "Nombre": self.inputs[0].text(),
                "Categoria": self.inputs[1].text(),                    
                "Disponibilidad": int(self.inputs[2].text()),
                "Precio": float(self.inputs[3].text()),
                }

            if all(datos.values()):
                try:
                    conexion.insertar_dato("Producto", datos)
                    QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el producto:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")

######################################################################################################
class EliminarProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliminar Producto")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/eliminarpr.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear el menú desplegable
        self.producto_combo = QComboBox(self)
        self.producto_combo.setFixedSize(317, 40)
        self.producto_combo.move(598, 194)
        self.producto_combo.setStyleSheet("""
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
                border-width: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #111A2D;
                color: #E6AA68;
                selection-background-color: #E6AA68;
                selection-color: #111A2D;
            }
        """)
        
        # Cargar productos desde la base de datos
        self.cargar_productos()
        
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

    def cargar_productos(self):
        # Primero agregamos un ítem por defecto
        self.producto_combo.addItem("Seleccionar producto")
        
        try:
            from conexion import mostrar_productos
            productos = mostrar_productos()
            # Agregamos solo los nombres de los productos al combo
            for producto in productos:
                self.producto_combo.addItem(producto[1])  # producto[1] es el nombre
        except Exception as e:
            print(f"Error al cargar productos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainWindow()  
            self.main_window.show()
            self.close()
        elif button.text() == "Confirmar":
            producto_seleccionado = self.producto_combo.currentText()
            if producto_seleccionado != "Seleccionar producto":
                try:
                    from conexion import eliminar_producto
                    eliminar_producto(producto_seleccionado)
                    QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                    self.cargar_productos()  # Recargamos la lista
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un producto")

##########################################################################################################
class EditarProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editar Producto")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/editarpr.png')
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
            self.main_window = MainWindow()  
            self.main_window.show()
            self.close()      
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
            productos = mostrar_productos()
            
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

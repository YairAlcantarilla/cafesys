import sys
import p_inicio
import conexion
import main_p
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
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

        button_configs = [
            ["Caja", 30, 152, 200, 50],
            ["Reportes", 30, 227, 200, 50],
            ["Productos", 30, 303, 200, 50],
            ["Personal", 30, 378, 200, 50],
            ["Inventario", 30, 454, 200, 50],
            ["Ajustes", 30, 530, 200, 50],
            ["Salir", 30, 605, 200, 50],
            #otrosbotones
            ["Agregar Producto", 273, 144, 343, 55],
            ["Eliminar", 273, 225, 343, 55],
            ["Editar", 273, 306, 343, 55],
            ["Lista", 273, 387, 343, 55],
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
            ["", 598, 194, 317, 40],
            ["", 598, 284, 317, 40],
            ["", 598, 374, 317, 40],
            ["", 994, 198, 250, 40],
             
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

        input_configs = [
            [".", 598, 194, 317, 40],
   
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
        #elif button.text()=="Confirmar":
    
##########################################################################################################
class EditarProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editar Producto")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/editarprn.png')
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
"""class ListaProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Producto")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/listadp.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #Lista
        mostrar_productos()
    #boton
        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
        ]
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet(
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
        )
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.main_window = MainWindow()  
            self.main_window.show()
            self.close() """
            

class ListaProducto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista de Productos")
        self.setFixedSize(650, 600)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(15, 15, 620, 400)  # Posición y tamaño
        self.table_widget.setColumnCount(5)  # Número de columnas
        self.table_widget.setHorizontalHeaderLabels([
            "ID", "Nombre", "Categoría", "Disponibilidad", "Precio",
        ])

        self.cargar_datos()

        # Botón para regresar
        self.btn_regresar = QPushButton("Regresar", self)
        self.btn_regresar.setGeometry(300, 520, 100, 40)
        self.btn_regresar.clicked.connect(self.cerrar_ventana)

    def cargar_datos(self):
        from conexion import mostrar_productos  # Importar la función de conexión
        datos = mostrar_productos()

        self.table_widget.setRowCount(len(datos))  # Establecer número de filas

        for fila, producto in enumerate(datos):
            for columna, valor in enumerate(producto):
                item = QTableWidgetItem(str(valor))
                self.table_widget.setItem(fila, columna, item)

    def cerrar_ventana(self):
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

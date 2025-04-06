import sys
import p_inicio
import main_p
import conexion
from conexion import mostrar_productos, obtener_precio_producto, agregar_descuento, obtener_descuentos
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
#####################################################
class MainDesc(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/menu_d.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        #boton
        button_configs = [
            ["AgregarD", 273, 144, 343, 55],
            ["EliminarD", 273, 225, 343, 55],
            ["EditarD", 273, 306, 343, 55],
            ["ListaD", 273, 387, 343, 55],
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
        elif button.text() == "AgregarD":
            self.main_window = AgregarDto()
            self.main_window.show()
            self.close()
        elif button.text() == "EditarD":
            self.main_window = EditarDto()
            self.main_window.show()
            self.close()
        elif button.text() == "ListaD":
            self.main_window = ListaDto()
            self.main_window.show()
            self.close()
        elif button.text() == "EliminarD":
            self.main_window = EliminarDescuento()
            self.main_window.show()
            self.close()
#################################################

class AgregarDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar Descuento")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/agregar dto.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # ComboBox para seleccionar producto
        self.producto = QComboBox(self)
        self.producto.setFixedSize(240, 40)
        self.producto.move(588, 194)
        self.producto.setStyleSheet(self.estilo_combo_box())
        self.producto.currentIndexChanged.connect(self.mostrar_precio)

        self.cargar_productos()

        # Campos de entrada (precio, descuento, precio final)
        self.precio = QLineEdit(self)
        self.precio.setFixedSize(240, 40)
        self.precio.move(588, 281)
        self.precio.setReadOnly(True)  # Solo lectura
        self.precio.setStyleSheet(self.estilo_input())

        self.descuento = QLineEdit(self)
        self.descuento.setFixedSize(240, 40)
        self.descuento.move(952, 194)
        self.descuento.setPlaceholderText("Porcentaje %")
        self.descuento.setStyleSheet(self.estilo_input())
        self.descuento.textChanged.connect(self.calcular_precio_final)

        self.precio_final = QLineEdit(self)
        self.precio_final.setFixedSize(240, 40)
        self.precio_final.move(952, 281)
        self.precio_final.setReadOnly(True)  # Solo lectura
        self.precio_final.setStyleSheet(self.estilo_input())

        # Botones
        self.boton_confirmar = QPushButton("Confirmar", self)
        self.boton_confirmar.setFixedSize(227, 78)
        self.boton_confirmar.move(798, 554)
        self.boton_confirmar.setStyleSheet(self.estilo_boton())
        self.boton_confirmar.clicked.connect(self.guardar_descuento)

        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(77, 70)
        self.boton_regresar.move(1270, 655)
        self.boton_regresar.setStyleSheet(self.estilo_boton())
        self.boton_regresar.clicked.connect(self.cerrar_ventana)

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

    def estilo_input(self):
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
        """Carga la lista de productos en el QComboBox."""
        try:
            productos = mostrar_productos()
            self.producto.addItem("Seleccione un producto")  # Placeholder
            for producto in productos:
                self.producto.addItem(producto[1])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {str(e)}")

    def mostrar_precio(self):
        """Carga el precio del producto seleccionado."""
        nombre_producto = self.producto.currentText()
        if nombre_producto and nombre_producto != "Seleccione un producto":
            try:
                precio = obtener_precio_producto(nombre_producto)
                self.precio.setText(f"${precio}")
                self.calcular_precio_final()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al obtener precio: {str(e)}")
        #else:
            #self.precio.setText("")
            #self.precio_final.setText("")

    def calcular_precio_final(self):
        """Calcula el precio final después del descuento."""
        try:
            precio = float(self.precio.text().replace("$", "").strip()) if self.precio.text() else 0
            descuento = float(self.descuento.text()) if self.descuento.text() else 0
            if descuento < 0 or descuento > 100:
                QMessageBox.warning(self, "Error", "El descuento debe estar entre 0% y 100%.")
                return
            precio_final = precio - (precio * descuento / 100)
            self.precio_final.setText(f"${precio_final:.2f}")
        except ValueError:
            self.precio_final.setText("")

    def guardar_descuento(self):
        """Guarda el descuento en la base de datos."""
        nombre_producto = self.producto.currentText()
        if nombre_producto == "Seleccione un producto" or not nombre_producto:
            QMessageBox.warning(self, "Error", "Seleccione un producto válido.")
            return

        try:
            float(self.precio.text().replace("$", "").strip())
            descuento = float(self.descuento.text()) if self.descuento.text() else 0
            precio_final = float(self.precio_final.text().replace("$", "").strip())

            agregar_descuento(nombre_producto, descuento, precio_final)
            QMessageBox.information(self, "Éxito", "Descuento agregado correctamente.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el descuento: {str(e)}")

    def cerrar_ventana(self):
        """Cierra la ventana y regresa al menú anterior."""
        self.main_window = MainDesc()
        self.main_window.show()
        self.close()


######################################################################################################
from conexion import mostrar_descuentos, eliminar_descuento  # Asegúrate de tener estas funciones en tu módulo

class EliminarDescuento(QMainWindow):
   # descuento_eliminado = pyqtSignal()  # Señal para notificar eliminación

    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ELIMP.png')  # Usa una imagen apropiada
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        self.setWindowTitle("Eliminar Descuento")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #000928;")

        # Label
        label = QLabel("Descuento:", self)
        label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        label.move(30, 152)

        # ComboBox
        self.descuento_combo = QComboBox(self)
        self.descuento_combo.setFixedSize(200, 30)
        self.descuento_combo.move(160, 150)
        self.descuento_combo.setStyleSheet("""
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

        self.cargar_descuentos()

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

    def cargar_descuentos(self):
        self.descuento_combo.addItem("Seleccionar descuento")

        try:
            descuentos = mostrar_descuentos()
            for descuento in descuentos:
                self.descuento_combo.addItem(str(descuento))  # Ya no se usa descuento[0]
        except Exception as e:
            print(f"Error al cargar descuentos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Eliminar":
            descuento_seleccionado = self.descuento_combo.currentText()
            if descuento_seleccionado != "Seleccionar descuento":
                try:
                    eliminar_descuento(descuento_seleccionado)

                    # Refrescar ventana principal si aplica
                    for widget in QApplication.topLevelWidgets():
                        if hasattr(widget, 'cargar_datos'):
                            widget.cargar_datos()
                            break

                    QMessageBox.information(self, "Éxito", "Descuento eliminado correctamente")
                    self.descuento_eliminado.emit()
                    self.descuento_combo.clear()
                    self.cargar_descuentos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el descuento:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un descuento")

######################################################################################################
class EditarDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agregar combo")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo agregar
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EditarD.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)


        input_configs = [
            [".", 588, 194, 240, 40],
            [".", 588, 281, 240, 40],
            [".", 952, 194, 240, 40],
            [".", 952, 281, 240, 40],
   
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
            self.main_window = MainDesc()  
            self.main_window.show()
            self.close()
#####################################################################################################

class ListaDto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Descuentos")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Fondo de pantalla
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ListaD.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Tabla para mostrar los descuentos
        self.tabla_descuentos = QTableWidget(self)
        self.tabla_descuentos.setColumnCount(4)
        self.tabla_descuentos.setHorizontalHeaderLabels(["ID",  "Descuento (%)", " ID Producto", "Precio Final"])
        self.tabla_descuentos.setFixedSize(800, 400)
        self.tabla_descuentos.move(280, 200)
        self.cargar_descuentos()

        # Botón de regreso
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.setFixedSize(77, 70)
        self.boton_regresar.move(1270, 655)
        self.boton_regresar.setStyleSheet(self.estilo_boton())
        self.boton_regresar.clicked.connect(self.regresar)

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


            
    def regresar(self):
        self.main_window = MainDesc()
        self.main_window.show()
        self.close()


    def cargar_descuentos(self):
        #Carga los descuentos desde la base de datos y los muestra en la tabla.
        try:
            descuentos = obtener_descuentos()
        
            if not descuentos:
                print("No hay descuentos para mostrar.")
                return

            self.tabla_descuentos.setRowCount(len(descuentos))
            for fila, descuento in enumerate(descuentos):
                for columna, dato in enumerate(descuento):
                    self.tabla_descuentos.setItem(fila, columna, QTableWidgetItem(str(dato)))

            self.tabla_descuentos.viewport().update()  # Asegura que la tabla se actualice visualmente
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar descuentos: {str(e)}")

    
#################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDesc()
    window.show()
    sys.exit(app.exec())
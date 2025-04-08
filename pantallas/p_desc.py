import sys
import p_inicio
import main_p
import conexion
from conexion import mostrar_productos, obtener_precio_producto, agregar_descuento, obtener_descuentos, mostrar_descuentos, conectar_db
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
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

        # Crear la tabla de descuentos
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)  # x, y, width, height
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "ID Descuento", "Producto", "Descuento (%)", "Precio Final"
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

        #boton
        button_configs = [
            ["AgregarD", 873, 144, 343, 55],
            ["EliminarD", 873, 225, 343, 55],
            ["EditarD", 873, 306, 343, 55],
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
            # Usar obtener_descuentos en lugar de consulta directa
            descuentos = obtener_descuentos()
            
            self.table_widget.setRowCount(len(descuentos))
            
            for fila, descuento in enumerate(descuentos):
                # Obtener el nombre del producto
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("SELECT Nombre FROM producto WHERE ID_producto = %s", (descuento[2],))
                nombre_producto = cursor.fetchone()[0]
                cursor.close()
                conexion.close()

                # ID Descuento
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(descuento[0])))
                # Nombre Producto
                self.table_widget.setItem(fila, 1, QTableWidgetItem(nombre_producto))
                # Porcentaje
                self.table_widget.setItem(fila, 2, QTableWidgetItem(f"{descuento[1]}%"))
                # Precio Final
                self.table_widget.setItem(fila, 3, QTableWidgetItem(f"${descuento[3]:.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los descuentos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            from main_p import MainPWindow  # Importar aquí para evitar importación circular
            self.main_window = MainPWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "AgregarD":
            self.ventana_agregar = AgregarDto(self)
            self.ventana_agregar.descuento_agregado.connect(self.cargar_datos)
            self.ventana_agregar.show()
        elif button.text() == "EliminarD":
            self.ventana_eliminar = EliminarDescuento(self)
            self.ventana_eliminar.descuento_eliminado.connect(self.cargar_datos)
            self.ventana_eliminar.show()
        elif button.text() == "EditarD":
            self.ventana_editar = EditarDto(self)
            self.ventana_editar.descuento_editado.connect(self.cargar_datos)
            self.ventana_editar.show()
        elif button.text() == "ListaD":
            self.ventana_lista = ListaDto(self)
            self.ventana_lista.show()
#################################################

class AgregarDto(QMainWindow):
    descuento_agregado = pyqtSignal()  # Nueva señal
    
    def __init__(self, parent=None):  # Añadir parent
        super().__init__(parent)
        
        self.setWindowTitle("Agregar Descuento")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #000928;")
        
        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Elementos de la interfaz
        producto_label = QLabel("Producto:")
        producto_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.producto = QComboBox()
        self.producto.setFixedSize(200, 30)
        self.producto.setStyleSheet(self.estilo_combo_box())
        
        precio_label = QLabel("Precio:")
        precio_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.precio = QLineEdit()
        self.precio.setReadOnly(True)
        self.precio.setStyleSheet(self.estilo_input())
        
        descuento_label = QLabel("Descuento (%):")
        descuento_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.descuento = QLineEdit()
        self.descuento.setStyleSheet(self.estilo_input())
        
        precio_final_label = QLabel("Precio Final:")
        precio_final_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.precio_final = QLineEdit()
        self.precio_final.setReadOnly(True)
        self.precio_final.setStyleSheet(self.estilo_input())
        
        # Botones
        button_layout = QHBoxLayout()  # Cambiar a QHBoxLayout
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_confirmar = QPushButton("Confirmar")
        
        # Añadir espaciado entre los botones
        button_layout.addStretch()  # Espacio flexible al inicio
        
        for btn in [self.btn_cancelar, self.btn_confirmar]:
            btn.setFixedSize(100, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E6AA68;
                    border-radius: 10px;
                    color: #111A2D;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #D69958;
                }
            """)
            button_layout.addWidget(btn)
            button_layout.addSpacing(10)  # Espacio entre botones
            
        button_layout.addStretch()  # Espacio flexible al final
        
        # Añadir widgets al layout
        layout.addWidget(producto_label)
        layout.addWidget(self.producto)
        layout.addWidget(precio_label)
        layout.addWidget(self.precio)
        layout.addWidget(descuento_label)
        layout.addWidget(self.descuento)
        layout.addWidget(precio_final_label)
        layout.addWidget(self.precio_final)
        layout.addLayout(button_layout)
        
        # Conexiones
        self.producto.currentIndexChanged.connect(self.mostrar_precio)
        self.descuento.textChanged.connect(self.calcular_precio_final)
        self.btn_cancelar.clicked.connect(self.close)
        self.btn_confirmar.clicked.connect(self.guardar_descuento)
        
        self.cargar_productos()

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
            self.descuento_agregado.emit()  # Emitir señal
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el descuento: {str(e)}")

######################################################################################################
from conexion import mostrar_descuentos, ocultar_descuento  # Asegúrate de tener estas funciones en tu módulo

class EliminarDescuento(QMainWindow):
    descuento_eliminado = pyqtSignal()

    def __init__(self, parent=None):  # Añadir parent
        super().__init__(parent)

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
        self.descuento_combo.clear()
        self.descuento_combo.addItem("Seleccionar descuento")

        try:
            descuentos = obtener_descuentos()  # Esta función ya filtra los descuentos ocultos
            for descuento in descuentos:
                self.descuento_combo.addItem(str(descuento[0]))
        except Exception as e:
            print(f"Error al cargar descuentos: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Cancelar":
            self.close()
        elif button.text() == "Eliminar":
            descuento_seleccionado = self.descuento_combo.currentText()
            if descuento_seleccionado != "Seleccionar descuento":
                reply = QMessageBox.question(
                    self,
                    'Confirmación',
                    '¿Está seguro de ocultar este descuento?\nNo estará disponible para su uso.',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        conexion.ocultar_descuento(descuento_seleccionado)

                        # Refrescar ventana principal si aplica
                        for widget in QApplication.topLevelWidgets():
                            if hasattr(widget, 'cargar_datos'):
                                widget.cargar_datos()
                                break

                        QMessageBox.information(self, "Éxito", "Descuento ocultado correctamente")
                        self.descuento_eliminado.emit()
                        self.descuento_combo.clear()
                        self.cargar_descuentos()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo ocultar el descuento:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un descuento")

######################################################################################################
class EditarDto(QMainWindow):
    descuento_editado = pyqtSignal()  # Añadir esta línea al inicio de la clase

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Editar Descuento")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #000928;")
        
        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ComboBox para seleccionar el descuento a editar
        descuento_label = QLabel("Seleccionar Descuento:")
        descuento_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.descuento_combo = QComboBox()
        self.descuento_combo.setFixedSize(200, 30)
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

        # Campos de edición
        porcentaje_label = QLabel("Porcentaje de Descuento:")
        porcentaje_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.porcentaje_input = QLineEdit()
        self.porcentaje_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #111A2D;
                color: #E6AA68;
            }
        """)

        precio_final_label = QLabel("Precio Final:")
        precio_final_label.setStyleSheet("color: #E6AA68; font-size: 16px;")
        self.precio_final_input = QLineEdit()
        self.precio_final_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                background-color: #111A2D;
                color: #E6AA68;
            }
        """)

        # Botones
        button_layout = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_confirmar = QPushButton("Confirmar")
        
        for btn in [self.btn_cancelar, self.btn_confirmar]:
            btn.setFixedSize(100, 30)
            btn.setStyleSheet("""
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
            button_layout.addWidget(btn)

        # Añadir widgets al layout
        layout.addWidget(descuento_label)
        layout.addWidget(self.descuento_combo)
        layout.addWidget(porcentaje_label)
        layout.addWidget(self.porcentaje_input)
        layout.addWidget(precio_final_label)
        layout.addWidget(self.precio_final_input)
        layout.addLayout(button_layout)

        # Conexiones
        self.btn_cancelar.clicked.connect(self.close)
        self.btn_confirmar.clicked.connect(self.guardar_cambios)
        self.descuento_combo.currentIndexChanged.connect(self.cargar_datos_descuento)

        # Cargar descuentos existentes
        self.cargar_descuentos()

    def cargar_descuentos(self):
        try:
            descuentos = mostrar_descuentos()
            self.descuento_combo.addItem("Seleccione un descuento")
            for descuento in descuentos:
                self.descuento_combo.addItem(str(descuento))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar descuentos: {str(e)}")

    def cargar_datos_descuento(self):
        descuento_id = self.descuento_combo.currentText()
        if descuento_id and descuento_id != "Seleccione un descuento":
            try:
                descuentos = obtener_descuentos()  # Usar el método existente
                for descuento in descuentos:
                    if str(descuento[0]) == descuento_id:  # Comparar con el ID seleccionado
                        self.porcentaje_input.setText(str(descuento[1]))  # Porcentaje
                        self.precio_final_input.setText(str(descuento[3]))  # Precio final
                        break
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar datos del descuento: {str(e)}")

    def guardar_cambios(self):
        descuento_id = self.descuento_combo.currentText()
        if descuento_id == "Seleccione un descuento":
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un descuento")
            return

        try:
            porcentaje = float(self.porcentaje_input.text())
            precio_final = float(self.precio_final_input.text())

            conexion = conectar_db()
            if conexion:
                cursor = conexion.cursor()
                sql = """
                    UPDATE descuentos 
                    SET Porcentaje = %s, Precio_final = %s 
                    WHERE ID_descuento = %s
                """
                cursor.execute(sql, (porcentaje, precio_final, descuento_id))
                conexion.commit()
                cursor.close()
                conexion.close()

                QMessageBox.information(self, "Éxito", "Descuento actualizado correctamente")
                self.descuento_editado.emit()
                self.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores numéricos válidos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar descuento: {str(e)}")

#####################################################################################################

class ListaDto(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        try:
            descuentos = obtener_descuentos()  # Esta función ya filtra los descuentos ocultos
        
            if not descuentos:
                print("No hay descuentos activos para mostrar.")
                return

            self.tabla_descuentos.setRowCount(len(descuentos))
            for fila, descuento in enumerate(descuentos):
                for columna, dato in enumerate(descuento):
                    self.tabla_descuentos.setItem(fila, columna, QTableWidgetItem(str(dato)))

            self.tabla_descuentos.viewport().update()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar descuentos: {str(e)}")

    
#################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDesc()
    window.show()
    sys.exit(app.exec())
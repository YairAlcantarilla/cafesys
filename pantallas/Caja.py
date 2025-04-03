import sys
import login
import p_inicio
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QMessageBox, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QSpinBox)
import conexion  # Add this import at the top of the file
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
        pixmap = QPixmap('imagenes/CAJAPR.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [
            ["Nombre del cliente", 825, 305, 150, 38],  # Changed from "Fecha"
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
            ["Confirmar", 842, 638, 94, 94],  
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
                    border-radius: 16px;
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
        self.table.setColumnCount(4)  # Changed from 3 to 4 columns
        self.table.setHorizontalHeaderLabels(['Producto', 'Fecha', 'Cantidad', 'Precio'])  # Added 'Precio'
        
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
        for column in range(4):  # Changed from 3 to 4
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

        # Añadir el visor de imágenes
        self.caja_imagenes = CajaImagenes(self)
        
        # Lista para almacenar datos temporales
        self.productos_temporales = []

    ######################  Tabla de contenido  ####################################################

    def button_clicked(self):
        button = self.sender()
        if button.text() == "PEfectivo":
            self.pago_efectivo_window = PagoEfectivoWindow(self)
            self.pago_efectivo_window.show()
            return
        elif button.text() == "Confirmar":
            if not self.productos_temporales:
                QMessageBox.warning(self, "Aviso", "No hay productos para confirmar")
                return
            
            # Generar ticket y obtener total
            total = self.generar_ticket()
            
            # Guardar la venta en la base de datos con forma de pago
            self.guardar_venta(forma_pago='Efectivo')  # Or get this from a payment method selection
            
            # Mostrar mensaje de confirmación
            QMessageBox.information(self, "Éxito", 
                f"Venta confirmada\nTotal: ${total:.2f}\nTicket generado correctamente")
            
            # Limpiar la tabla y los productos temporales
            self.limpiar_tabla()
            self.productos_temporales.clear()
            
            return
        elif button.text() == "Bebida":
            self.ventana_bebidas = VentanaBebidas(self)
            self.ventana_bebidas.show()
            return  # Don't call fade_out for this button
        elif button.text() == "Comida":
            self.ventana_comida = VentanaComida(self)
            self.ventana_comida.show()
            return  # Don't call fade_out for this button
        elif button.text() == "Regresar":
            self.cambioP = login.LoginWindow()
            self.fade_out()
        elif button.text() == "Ccompra":
            self.cambioP = CajaFinal()
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

    def agregar_producto_temporal(self, producto, fecha, cantidad, precio_total):
        # Agregar a la lista temporal
        self.productos_temporales.append({
            'producto': producto,
            'fecha': fecha,
            'cantidad': cantidad,
            'precio': precio_total
        })
        
        # Actualizar tabla
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        self.table.setItem(row_position, 0, QTableWidgetItem(producto))
        self.table.setItem(row_position, 1, QTableWidgetItem(fecha))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(cantidad)))
        self.table.setItem(row_position, 3, QTableWidgetItem(f"${precio_total:.2f}"))

    def guardar_venta(self, forma_pago='Efectivo', id_usuario=None):
        try:
            # Get valid user ID from connection
            if id_usuario is None:
                id_usuario = conexion.obtener_usuario_activo()  # We'll create this method
                if id_usuario is None:
                    raise Exception("No hay usuario válido para la venta")

            # Este método se llamaría cuando se finalice la venta
            for producto in self.productos_temporales:
                datos_venta = {
                    'producto': producto['producto'],
                    'fecha': producto['fecha'],
                    'cantidad': producto['cantidad'],
                    'precio_total': producto['precio'],
                    'forma_pago': forma_pago,
                    'id_usuario': id_usuario
                }
                
                # Debug: Imprimir datos antes de enviar
                print("Datos enviados a insertar_venta:")
                for key, value in datos_venta.items():
                    print(f"{key}: {value} ({type(value)})")
                    
                conexion.insertar_venta(datos_venta)
            
            # Limpiar datos temporales y tabla
            self.productos_temporales.clear()
            self.table.setRowCount(0)
            
            QMessageBox.information(self, "Éxito", "Venta registrada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la venta: {str(e)}")

    def generar_ticket(self):
        """Genera un ticket de compra con los productos y totales"""
        if not self.productos_temporales:
            QMessageBox.warning(self, "Aviso", "No hay productos para generar ticket")
            return

        total_venta = 0
        total_articulos = 0
        ticket_text = []
        
        # Get customer name from input
        nombre_cliente = self.inputs[0].text() or "Cliente General"

        # Encabezado del ticket
        ticket_text.append("=" * 40)
        ticket_text.append("CAFETERÍA SISTEMA")
        ticket_text.append("=" * 40)
        ticket_text.append(f"Fecha: {QDate.currentDate().toString('dd/MM/yyyy')}")
        ticket_text.append(f"Cliente: {nombre_cliente}")
        ticket_text.append("-" * 40)
        ticket_text.append("PRODUCTO          CANT    PRECIO    TOTAL")
        ticket_text.append("-" * 40)

        # Agregar productos
        for producto in self.productos_temporales:
            nombre = producto['producto'][:15].ljust(15)  # Limitar longitud del nombre
            cantidad = str(producto['cantidad']).center(8)
            precio_unit = f"${producto['precio']/producto['cantidad']:.2f}".rjust(8)
            total = f"${producto['precio']:.2f}".rjust(8)
            
            ticket_text.append(f"{nombre}{cantidad}{precio_unit}{total}")
            
            total_venta += producto['precio']
            total_articulos += producto['cantidad']

        # Agregar totales
        ticket_text.append("-" * 40)
        ticket_text.append(f"Total Artículos: {total_articulos}")
        ticket_text.append(f"Total a Pagar: ${total_venta:.2f}")
        ticket_text.append("=" * 40)
        ticket_text.append("¡Gracias por su compra!")
        ticket_text.append("=" * 40)

        # Guardar el ticket en un archivo
        try:
            with open('ticket.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(ticket_text))
            QMessageBox.information(self, "Éxito", "Ticket generado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar ticket: {str(e)}")

        return total_venta

###############################################################################################
class CajaImagenes(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(1150, 85, 220, 683)  
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Configurar el estilo
        self.setStyleSheet("""
            QGraphicsView {
                border: none;
                background: transparent;
            }
        """)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        # Lista de imágenes para rotar
        self.imagenes = ["imagenes/Promo3.png", "imagenes/Promo5.png"]
        self.indice_actual = 0

        self.cambiar_imagen()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cambiar_imagen)
        self.timer.start(3000)

    def cambiar_imagen(self):
        """Cambia la imagen en la caja cada cierto tiempo."""
        if self.imagenes:
            pixmap = QPixmap(self.imagenes[self.indice_actual])
            pixmap = pixmap.scaled(216, 680, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            self.image_item.setPixmap(pixmap)

            # Avanzar al siguiente índice
            self.indice_actual = (self.indice_actual + 1) % len(self.imagenes)

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
class VentanaBebidas(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Bebida")
        self.setFixedSize(400, 200)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Dropdown para bebidas
        self.bebida_combo = QComboBox()
        self.bebida_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                min-height: 30px;
            }
        """)
        self.cargar_bebidas()
        
        # Spinbox para cantidad
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                min-height: 30px;
            }
        """)
        
        # Botón agregar
        self.agregar_btn = QPushButton("Agregar")
        self.agregar_btn.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
                padding: 5px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
        """)
        
        layout.addWidget(QLabel("Seleccionar Bebida:"))
        layout.addWidget(self.bebida_combo)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_spin)
        layout.addWidget(self.agregar_btn)
        
        self.agregar_btn.clicked.connect(self.agregar_bebida)

    def cargar_bebidas(self):
        connection = None
        try:
            connection = conexion.conectar_db()
            if connection is None:
                raise Exception("No se pudo establecer conexión con la base de datos")
                
            cursor = connection.cursor()
            # Cambiar 'Bebida' a 'Bebidas'
            cursor.execute("SELECT Nombre FROM Producto WHERE Categoria = 'Bebidas'")
            bebidas = cursor.fetchall()
            
            if bebidas:
                self.bebida_combo.addItems([bebida[0] for bebida in bebidas])
            else:
                QMessageBox.warning(self, "Aviso", "No hay bebidas disponibles")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar bebidas: {str(e)}")
        finally:
            if connection:
                connection.close()

    def agregar_bebida(self):
        bebida = self.bebida_combo.currentText()
        cantidad = self.cantidad_spin.value()
        precio = conexion.obtener_precio_producto(bebida)
        
        if precio is not None:
            precio_total = precio * cantidad
            # Obtener la fecha actual
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")
            
            # Enviar datos a la ventana principal
            self.parent().agregar_producto_temporal(bebida, fecha_actual, cantidad, precio_total)
            self.close()

#########################################################################################################
class VentanaComida(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Comida")
        self.setFixedSize(400, 200)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Dropdown para comidas
        self.comida_combo = QComboBox()
        self.comida_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                min-height: 30px;
            }
        """)
        self.cargar_comidas()
        
        # Spinbox para cantidad
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                min-height: 30px;
            }
        """)
        
        # Botón agregar
        self.agregar_btn = QPushButton("Agregar")
        self.agregar_btn.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
                padding: 5px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
        """)
        
        layout.addWidget(QLabel("Seleccionar Comida:"))
        layout.addWidget(self.comida_combo)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_spin)
        layout.addWidget(self.agregar_btn)
        
        self.agregar_btn.clicked.connect(self.agregar_comida)

    def cargar_comidas(self):
        connection = None
        try:
            connection = conexion.conectar_db()
            if connection is None:
                raise Exception("No se pudo establecer conexión con la base de datos")
                
            cursor = connection.cursor()
            cursor.execute("SELECT Nombre FROM Producto WHERE Categoria = 'Comida'")
            comidas = cursor.fetchall()
            
            if comidas:
                self.comida_combo.addItems([comida[0] for comida in comidas])
            else:
                QMessageBox.warning(self, "Aviso", "No hay comidas disponibles")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar comidas: {str(e)}")
        finally:
            if connection:
                connection.close()

    def agregar_comida(self):
        comida = self.comida_combo.currentText()
        cantidad = self.cantidad_spin.value()
        precio = conexion.obtener_precio_producto(comida)
        
        if precio is not None:
            precio_total = precio * cantidad
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")
            
            self.parent().agregar_producto_temporal(comida, fecha_actual, cantidad, precio_total)
            self.close()

#########################################################################################################
class CajaFinal(QMainWindow):
    pass
##############
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CajaI()
    window.show()
    sys.exit(app.exec())


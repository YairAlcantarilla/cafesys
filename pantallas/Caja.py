import sys
import login
import p_inicio
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QMessageBox, QLineEdit, 
                           QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QSpinBox)
import conexion 
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
        pixmap = QPixmap('imagenes/CAJAFINAL.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        input_configs = [
            ["Nombre del cliente", 825, 318, 150, 38],  
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
            ["PEfectivo", 914, 443, 77, 75],
            ["PTarjeta", 1015, 443, 77, 75],
            ["Ayuda", 1210, 25, 50, 50],
            ["Confirmar", 842, 638, 94, 94],
            ["Borrar", 942, 638, 94, 94],  # Nuevo botón Borrar
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
            # Agregar estilo específico para el botón Borrar
            if button.text() == "Borrar":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 0px solid #E6AA68;
                        border-radius: 16px;
                        color: transparent;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(230, 170, 104, 0.2);
                    }
                    QPushButton:pressed {
                        background-color: rgba(230, 170, 104, 0.4);
                    }
                """)
            self.buttons.append(button)
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

        ######################  Tabla de contenido  ####################################################
        self.table = QTableWidget(self)
        self.table.setGeometry(40, 125, 618, 605) 
        self.table.setColumnCount(4) 
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
        for column in range(4): 
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)

        # Configurar selección de filas
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Añadir el visor de imágenes
        self.caja_imagenes = CajaImagenes(self)
        
        # Lista para almacenar datos temporales
        self.productos_temporales = []

    ######################  Tabla de contenido  ####################################################

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Borrar":
            self.borrar_producto()
            return
        if button.text() == "PEfectivo":

            if not self.productos_temporales:
                QMessageBox.warning(self, "Aviso", "Agregue productos antes de proceder al pago")
                return
            self.pago_efectivo_window = PagoEfectivoWindow(self)
            self.pago_efectivo_window.show()
            return
        elif button.text() == "Confirmar":
            if not self.productos_temporales:
                QMessageBox.warning(self, "Aviso", "No hay productos para confirmar")
                return

            if not hasattr(self, 'efectivo_recibido'):
                QMessageBox.warning(self, "Aviso", "Primero debe ingresar el pago")
                return
            
            try:
                # Convert all values to float consistently
                total = sum(float(str(producto['precio'])) for producto in self.productos_temporales)
                efectivo = float(self.efectivo_recibido)
                
                if efectivo < total:
                    QMessageBox.warning(self, "Error", "El efectivo recibido es insuficiente")
                    return

                self.guardar_venta(forma_pago='Efectivo')
                total_venta = self.generar_ticket()
                
                if total_venta > 0:
                    cambio = float(self.cambio_calculado)
                    QMessageBox.information(self, "Éxito", 
                        f"Venta confirmada\nTotal: ${total_venta:.2f}\n"
                        f"Efectivo: ${efectivo:.2f}\n"
                        f"Cambio: ${cambio:.2f}\n"
                        "Ticket generado correctamente")
                
                    self.limpiar_tabla()
                    self.productos_temporales.clear()
                    if hasattr(self, 'pago_efectivo_window'):
                        self.pago_efectivo_window.close()
                    delattr(self, 'efectivo_recibido')
                    delattr(self, 'cambio_calculado')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al procesar la venta: {str(e)}")
            return
        elif button.text() == "Bebida":
            self.ventana_bebidas = VentanaBebidas(self)
            self.ventana_bebidas.show()
            return
        elif button.text() == "Comida":
            self.ventana_comida = VentanaComida(self)
            self.ventana_comida.show()
            return 
        elif button.text() == "Combos":
            self.ventana_combos = VentanaCombos(self)
            self.ventana_combos.show()
            return
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
        # Verificar si hay descuento activo
        producto_id = conexion.obtener_producto_id(producto)
        if producto_id:
            descuento = conexion.obtener_descuento_activo(producto_id)
            
            if descuento:
                porcentaje, precio_final = descuento
                # Calcular precio con descuento
                precio_unitario = precio_total / cantidad
                precio_con_descuento = precio_final * cantidad
                
                # Mostrar mensaje de descuento aplicado
                QMessageBox.information(
                    self,
                    "Descuento Aplicado",
                    f"¡Se aplicó un descuento del {porcentaje}%!\n"
                    f"Precio original: ${precio_total:.2f}\n"
                    f"Precio con descuento: ${precio_con_descuento:.2f}"
                )
                
                # Actualizar precio total con descuento
                precio_total = precio_con_descuento

        # Agregar a la lista de productos temporales
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
            if id_usuario is None:
                id_usuario = 250103

            for producto in self.productos_temporales:
                datos_venta = {
                    'producto': producto['producto'],
                    'fecha': QDate.currentDate().toString('yyyy-MM-dd'),
                    'cantidad': producto['cantidad'],
                    'precio_total': producto['precio'],
                    'forma_pago': forma_pago,
                    'id_usuario': id_usuario
                }

                if not conexion.insertar_venta(datos_venta):
                    raise Exception("Error al insertar la venta en la base de datos")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la venta: {str(e)}")
            raise e

    def generar_ticket(self):
        """Genera un ticket de compra con los productos y totales"""
        try:
            if not self.productos_temporales:
                QMessageBox.warning(self, "Aviso", "No hay productos para generar ticket")
                return 0.0

            # Convertir todos los precios a float antes de sumar
            total_venta = sum(float(str(producto['precio'])) for producto in self.productos_temporales)
            total_articulos = sum(producto['cantidad'] for producto in self.productos_temporales)
            
            nombre_cliente = self.inputs[0].text() or "Cliente General"

            ticket_text = [
                "=" * 40,
                "CAFETERÍA SISTEMA",
                "=" * 40,
                f"Fecha: {QDate.currentDate().toString('dd/MM/yyyy')}",
                f"Cliente: {nombre_cliente}",
                "-" * 40,
                "PRODUCTO          CANT    PRECIO    TOTAL",
                "-" * 40
            ]

            for producto in self.productos_temporales:
                nombre = producto['producto'][:15].ljust(15)
                cantidad = str(producto['cantidad']).center(8)
                precio_unit = f"${float(str(producto['precio']))/producto['cantidad']:.2f}".rjust(8)
                total = f"${float(str(producto['precio'])):.2f}".rjust(8)
                ticket_text.append(f"{nombre}{cantidad}{precio_unit}{total}")

            ticket_text.extend([
                "-" * 40,
                f"Total Artículos: {total_articulos}",
                f"Total a Pagar: ${total_venta:.2f}",
                "-" * 40,
                f"Efectivo Recibido: ${float(self.efectivo_recibido):.2f}",
                f"Cambio: ${float(self.cambio_calculado):.2f}",
                "=" * 40,
                "¡Gracias por su compra!",
                "=" * 40
            ])

            with open('ticket.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(ticket_text))

            return total_venta

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar ticket: {str(e)}")
            return 0.0

    def borrar_producto(self):
        """Borra el producto seleccionado de la tabla y de la lista temporal"""
        filas_seleccionadas = self.table.selectedIndexes()
        if not filas_seleccionadas:
            QMessageBox.warning(self, "Aviso", "Por favor seleccione un producto para borrar")
            return

        # Obtener índices únicos de las filas seleccionadas
        filas_unicas = set(index.row() for index in filas_seleccionadas)
        
        # Confirmar la eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar {len(filas_unicas)} producto(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            # Borrar desde el último índice para no afectar los índices anteriores
            for fila in sorted(filas_unicas, reverse=True):
                del self.productos_temporales[fila]
                self.table.removeRow(fila)

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
        self.setStyleSheet("""
            QDialog {
                background-color: #192745;
            }
            QLabel {
                color: #E6AA68;
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                font-size: 14px;
                min-height: 30px;
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Calcular total a pagar manejando Decimal
        try:
            self.total_a_pagar = float(sum(float(str(producto['precio'])) for producto in parent.productos_temporales))
        except (ValueError, TypeError, KeyError) as e:
            QMessageBox.critical(self, "Error", f"Error al calcular el total: {str(e)}")
            self.total_a_pagar = 0.0

        # Campo de total a pagar (no editable)
        layout.addWidget(QLabel("Total a Pagar:"))
        self.total_field = QLineEdit()
        self.total_field.setReadOnly(True)
        self.total_field.setText(f"${self.total_a_pagar:.2f}")
        layout.addWidget(self.total_field)

        # Campo para efectivo recibido
        layout.addWidget(QLabel("Efectivo Recibido:"))
        self.efectivo_field = QLineEdit()
        self.efectivo_field.setPlaceholderText("Ingrese el monto recibido")
        self.efectivo_field.textChanged.connect(self.calcular_cambio)
        layout.addWidget(self.efectivo_field)

        # Campo para mostrar el cambio (no editable)
        layout.addWidget(QLabel("Cambio:"))
        self.cambio_field = QLineEdit()
        self.cambio_field.setReadOnly(True)
        layout.addWidget(self.cambio_field)

        # Agregar botón de guardar
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
                padding: 8px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
        """)
        self.guardar_btn.clicked.connect(self.guardar_pago)
        layout.addWidget(self.guardar_btn)

    def calcular_cambio(self):
        try:
            efectivo = float(self.efectivo_field.text() or 0)
            cambio = efectivo - self.total_a_pagar
            self.cambio_field.setText(f"${cambio:.2f}")
            self.guardar_btn.setEnabled(cambio >= 0)
        except ValueError:
            self.cambio_field.setText("Error")
            self.guardar_btn.setEnabled(False)

    def guardar_pago(self):
        try:
            efectivo = float(self.efectivo_field.text() or 0)
            if efectivo < self.total_a_pagar:
                QMessageBox.warning(self, "Error", "El efectivo recibido es insuficiente")
                return
            self.parent().efectivo_recibido = efectivo
            self.parent().cambio_calculado = efectivo - self.total_a_pagar
            
            QMessageBox.information(self, "Éxito", "Pago guardado. Presione 'Confirmar' para finalizar la venta.")
            self.close()
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese un monto válido")

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
        self.bebida_combo.currentTextChanged.connect(self.actualizar_stock_disponible)

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

    def actualizar_stock_disponible(self, bebida):
        if bebida:
            stock = conexion.obtener_stock_producto(bebida)
            self.cantidad_spin.setMaximum(stock)
            if stock == 0:
                self.agregar_btn.setEnabled(False)
                QMessageBox.warning(self, "Sin Stock", f"No hay stock disponible de {bebida}")
            else:
                self.agregar_btn.setEnabled(True)

    def agregar_bebida(self):
        bebida = self.bebida_combo.currentText()
        
        if bebida == "Bebidas" or not bebida:
            QMessageBox.warning(self, "Error", "Por favor seleccione un producto")
            return
            
        cantidad = self.cantidad_spin.value()
        stock_actual = conexion.obtener_stock_producto(bebida)
        
        if stock_actual < cantidad:
            QMessageBox.warning(self, "Error", f"Stock insuficiente. Solo hay {stock_actual} unidades disponibles")
            return
            
        precio = conexion.obtener_precio_producto(bebida)
        
        if precio is not None:
            precio_total = precio * cantidad
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")
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
        self.comida_combo.currentTextChanged.connect(self.actualizar_stock_disponible)

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

    def actualizar_stock_disponible(self, comida):
        if comida:
            stock = conexion.obtener_stock_producto(comida)
            self.cantidad_spin.setMaximum(stock)
            if stock == 0:
                self.agregar_btn.setEnabled(False)
                QMessageBox.warning(self, "Sin Stock", f"No hay stock disponible de {comida}")
            else:
                self.agregar_btn.setEnabled(True)

    def agregar_comida(self):
        comida = self.comida_combo.currentText()
        
        if comida == "Comida" or not comida:
            QMessageBox.warning(self, "Error", "Por favor seleccione un producto")
            return
            
        cantidad = self.cantidad_spin.value()
        stock_actual = conexion.obtener_stock_producto(comida)
        
        if stock_actual < cantidad:
            QMessageBox.warning(self, "Error", f"Stock insuficiente. Solo hay {stock_actual} unidades disponibles")
            return
            
        precio = conexion.obtener_precio_producto(comida)
        
        if precio is not None:
            precio_total = precio * cantidad
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")
            self.parent().agregar_producto_temporal(comida, fecha_actual, cantidad, precio_total)
            self.close()

#########################################################################################################
class VentanaCombos(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Combo")
        self.setFixedSize(400, 200)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Dropdown para combos
        self.combo_combo = QComboBox()
        self.combo_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
                min-height: 30px;
            }
        """)
        self.cargar_combos()
        
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
        
        # Labels con estilo
        label_combo = QLabel("Seleccionar Combo:")
        label_cantidad = QLabel("Cantidad:")
        label_combo.setStyleSheet("color: #E6AA68;")
        label_cantidad.setStyleSheet("color: #E6AA68;")
        
        layout.addWidget(label_combo)
        layout.addWidget(self.combo_combo)
        layout.addWidget(label_cantidad)
        layout.addWidget(self.cantidad_spin)
        layout.addWidget(self.agregar_btn)
        
        self.agregar_btn.clicked.connect(self.agregar_combo)

    def cargar_combos(self):
        try:
            # Inicializar el diccionario de combos
            self.combos_info = {}
            
            combos = conexion.mostrar_combos()
            if combos:
                nombres_combos = []
                for combo in combos:
                    nombre = combo[0]
                    productos = combo[1].split(',') if combo[1] else []
                    precio = combo[2]
                    
                    # Guardar la información del combo
                    self.combos_info[nombre] = {
                        'productos': productos,
                        'precio': precio
                    }
                    nombres_combos.append(nombre)
                
                self.combo_combo.addItems(nombres_combos)
            else:
                QMessageBox.warning(self, "Aviso", "No hay combos disponibles")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar combos: {str(e)}")

    def agregar_combo(self):
        combo_nombre = self.combo_combo.currentText()
        cantidad = self.cantidad_spin.value()
        
        if combo_nombre in self.combos_info:
            combo_info = self.combos_info[combo_nombre]
            precio_total = combo_info['precio'] * cantidad
            fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")
            
            # Agregar el combo como un producto
            self.parent().agregar_producto_temporal(
                combo_nombre, 
                fecha_actual, 
                cantidad, 
                float(precio_total)  # Convertir Decimal a float
            )
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Por favor seleccione un combo válido")

#########################################################################################################
class CajaFinal(QMainWindow):
    pass
##############
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CajaI()
    window.show()
    sys.exit(app.exec())


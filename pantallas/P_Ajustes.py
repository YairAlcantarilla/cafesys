import sys
import p_inicio
import conexion
from PyQt6.QtCore import Qt, QPropertyAnimation
import p_inicio, Caja, P_Registros, main_p, personal, login, p_inventario
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QGraphicsOpacityEffect, QLineEdit,
                           QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                           QRadioButton, QButtonGroup, QGridLayout, QComboBox, QFileDialog)
import subprocess
import os
from datetime import datetime
import json



class MainAjustes(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/PAJUSTES.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        ###############################################
        button_configs = [
            ["Caja", 30, 152, 60, 50],
            ["Reportes", 30, 227, 60, 50],
            ["Productos", 30, 303, 60, 50],
            ["Personal", 30, 378, 60, 50],
            ["Inventario", 30, 454, 60, 50],
            ["Ajustes", 30, 530, 60, 50],
            ["Salir", 30, 605, 60, 50],
            #################################
            ["Exportar R", 168, 135, 344, 55],
            ["Importar R", 168, 215, 344, 55],
            ["ExportarRepo", 168, 296, 344, 55], 
            ["RegresarE", 1270, 655, 77, 70],
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
                background-color: rgba(255, 255, 255, 20);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 80);
            }
        """)
            self.buttons.append(button)
        
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)
        
        # Time selector section
        # Labels
        self.time_label = QLabel("Configurar hora:", self)
        self.time_label.setGeometry(168, 456, 344, 30)  # 476 - 20
        self.time_label.setStyleSheet("""
            QLabel {
                color: #E6AA68;
                font-size: 14px;
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hours dropdown
        self.hours_combo = QComboBox(self)
        self.hours_combo.setGeometry(168, 496, 165, 40)  # 516 - 20
        self.hours_combo.addItems([f"{i:02d}" for i in range(24)])  # 00-23 hours
        
        # Minutes dropdown
        self.minutes_combo = QComboBox(self)
        self.minutes_combo.setGeometry(347, 496, 165, 40)  # 516 - 20
        self.minutes_combo.addItems([f"{i:02d}" for i in range(60)])  # 00-59 minutes

        # Style for both dropdowns
        time_style = """
            QComboBox {
                border: 1px solid #E6AA68;
                border-radius: 10px;
                padding: 5px;
                background-color: #111A2D;
                color: #E6AA68;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(imagenes/down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #111A2D;
                color: #E6AA68;
                selection-background-color: #E6AA68;
                selection-color: #111A2D;
            }
        """
        self.hours_combo.setStyleSheet(time_style)
        self.minutes_combo.setStyleSheet(time_style)

        # Confirm button
        self.set_time_button = QPushButton("Establecer Hora", self)
        self.set_time_button.setGeometry(168, 546, 344, 40)  # 566 - 20
        self.set_time_button.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 0.3);
            }
        """)
        self.set_time_button.clicked.connect(self.set_time)
    
    def button_clicked(self):
        button = self.sender()

        if button.text() == "Exportar R":
            # Confirmación antes de exportar
            respuesta = QMessageBox.question(
                self,
                "Confirmar exportación",
                "¿Desea crear un respaldo de la base de datos?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                self.exportar_base_datos()
                
        elif button.text() == "Importar R":
            # Confirmación antes de importar
            respuesta = QMessageBox.question(
                self,
                "Confirmar importación",
                "¿Desea restaurar la base de datos desde un respaldo?\n"
                "ADVERTENCIA: Esta acción reemplazará todos los datos actuales.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                self.importar_base_datos()

        elif button.text() == "ExportarRepo":
            self.exportar_reportes_excel()

        elif button.text() == "RegresarE":
            self.cambioP = p_inicio.MainWindow()
            self.fade_out()
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
    
    def set_time(self):
        hours = self.hours_combo.currentText()
        minutes = self.minutes_combo.currentText()
        selected_time = f"{hours}:{minutes}"
        
        try:
            # Guardar la hora configurada en un archivo JSON
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            config = {'scheduled_time': selected_time}
            
            with open(config_path, 'w') as f:
                json.dump(config, f)
            
            QMessageBox.information(
                self,
                "Hora Configurada",
                f"Hora establecida: {selected_time}\nLos reportes se generarán automáticamente a esta hora."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al establecer la hora: {str(e)}"
            )

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
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()

    def exportar_base_datos(self):
        try:
            from conexion import obtener_credenciales_db
            
            # Obtener credenciales directamente del módulo de conexión
            credenciales = obtener_credenciales_db()
            DB_NAME = credenciales['database']
            DB_USER = credenciales['user']
            DB_PASS = credenciales['passwd']
            DB_HOST = credenciales['host']

            # Crear nombre de archivo con fecha
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"backup_tienda_{fecha_actual}.sql"

            # Abrir diálogo para seleccionar ubicación
            ruta_guardar = QFileDialog.getSaveFileName(
                self,
                "Guardar respaldo",
                nombre_archivo,
                "SQL files (*.sql)"
            )[0]

            if ruta_guardar:
                # Comando para respaldar la base de datos
                comando = f'mysqldump -h {DB_HOST} -u {DB_USER}'
                if DB_PASS:
                    comando += f' -p{DB_PASS}'
                comando += f' {DB_NAME} > "{ruta_guardar}"'

                proceso = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if proceso.returncode == 0:
                    QMessageBox.information(
                        self,
                        "Éxito",
                        f"Base de datos respaldada exitosamente en:\n{ruta_guardar}"
                    )
                else:
                    raise Exception(f"Error en mysqldump: {proceso.stderr}")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al respaldar la base de datos:\n{str(e)}"
            )

    def importar_base_datos(self):
        try:
            from conexion import obtener_credenciales_db
            
            # Obtener credenciales directamente del módulo de conexión
            credenciales = obtener_credenciales_db()
            DB_NAME = credenciales['database']
            DB_USER = credenciales['user']
            DB_PASS = credenciales['passwd']
            DB_HOST = credenciales['host']

            # Abrir diálogo para seleccionar archivo
            ruta_archivo = QFileDialog.getOpenFileName(
                self,
                "Seleccionar archivo de respaldo",
                "",
                "SQL files (*.sql)"
            )[0]

            if ruta_archivo:
                # Comando para restaurar la base de datos
                comando = f'mysql -h {DB_HOST} -u {DB_USER}'
                if DB_PASS:
                    comando += f' -p{DB_PASS}'
                comando += f' {DB_NAME} < "{ruta_archivo}"'

                proceso = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if proceso.returncode == 0:
                    QMessageBox.information(
                        self,
                        "Éxito",
                        "Base de datos restaurada exitosamente"
                    )
                else:
                    raise Exception(f"Error en mysql: {proceso.stderr}")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al restaurar la base de datos:\n{str(e)}"
            )

    def exportar_reportes_excel(self):
        try:
            import pandas as pd
            from conexion import conectar_db
            from datetime import datetime
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

            # Obtener fecha y hora actual
            now = datetime.now()
            fecha_actual = now.strftime("%d/%m/%Y")
            hora_actual = now.strftime("%H:%M:%S")
            dia_semana = now.strftime("%A")
            
            # Traducir día de la semana al español
            dias = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
            }
            dia_semana = dias.get(dia_semana, dia_semana)

            # Conectar a la base de datos
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            # Verificar si existen ventas del día
            cursor.execute("SELECT COUNT(*) FROM ventas WHERE DATE(fecha) = CURDATE()")
            ventas_count = cursor.fetchone()[0]
            
            if ventas_count == 0:
                raise Exception("No hay ventas registradas para el día de hoy")
            
            # Obtener todas las ventas del día con su información de total
            try:
                cursor.execute("""
                    SELECT id_venta, fecha, total
                    FROM ventas
                    WHERE DATE(fecha) = CURDATE()
                    ORDER BY fecha
                """)
                ventas_dia = cursor.fetchall()
            except Exception:
                # Si no existe la columna 'total', intentar determinar cuál es
                cursor.execute("DESCRIBE ventas")
                columnas_ventas = cursor.fetchall()
                columnas_nombres = [col[0] for col in columnas_ventas]
                
                posibles_columnas_total = ['total', 'monto', 'importe', 'precio_total', 'valor_total', 'monto_total']
                columna_total = None
                
                for col in posibles_columnas_total:
                    if col in columnas_nombres:
                        columna_total = col
                        break
                
                if not columna_total:
                    # Si no se encuentra ninguna columna adecuada, usar un valor fijo
                    cursor.execute("""
                        SELECT id_venta, fecha, 0 as total
                        FROM ventas
                        WHERE DATE(fecha) = CURDATE()
                        ORDER BY fecha
                    """)
                else:
                    # Usar la columna encontrada
                    cursor.execute(f"""
                        SELECT id_venta, fecha, {columna_total} as total
                        FROM ventas
                        WHERE DATE(fecha) = CURDATE()
                        ORDER BY fecha
                    """)
            
            ventas_dia = cursor.fetchall()
        
            # Lista para almacenar información detallada por venta
            ventas_detalladas = []
            importe_total_dia = 0
            
            # Verificar si existe la tabla clientes
            cursor.execute("SHOW TABLES")
            tablas = [tabla[0] for tabla in cursor.fetchall()]
            tiene_tabla_clientes = 'clientes' in tablas or 'cliente' in tablas
            
            # Para cada venta, obtener todos los detalles y la info del cliente
            for venta in ventas_dia:
                id_venta, fecha_venta, total_venta = venta
                importe_total_dia += float(total_venta) if total_venta is not None else 0
                
                # Información de la venta
                info_venta = {
                    'id_venta': id_venta,
                    'fecha': fecha_venta.strftime('%d/%m/%Y %H:%M:%S') if hasattr(fecha_venta, 'strftime') else str(fecha_venta),
                    'total': float(total_venta) if total_venta is not None else 0,
                    'productos': [],
                    'cliente': 'No registrado'
                }
                
                # Intentar obtener información del cliente
                if tiene_tabla_clientes:
                    try:
                        # Verificar si existe relación con clientes en ventas
                        cursor.execute("DESCRIBE ventas")
                        cols_ventas = [col[0].lower() for col in cursor.fetchall()]
                        
                        if 'id_cliente' in cols_ventas or 'cliente_id' in cols_ventas:
                            col_cliente = 'id_cliente' if 'id_cliente' in cols_ventas else 'cliente_id'
                            
                            tabla_cliente = 'clientes' if 'clientes' in tablas else 'cliente'
                            
                            cursor.execute(f"""
                                SELECT c.nombre, c.apellido, c.telefono
                                FROM ventas v
                                JOIN {tabla_cliente} c ON v.{col_cliente} = c.id_{tabla_cliente[:-1] if tabla_cliente.endswith('s') else tabla_cliente}
                                WHERE v.id_venta = %s
                            """, (id_venta,))
                            
                            cliente = cursor.fetchone()
                            if cliente:
                                nombre, apellido, telefono = cliente
                                info_venta['cliente'] = f"{nombre} {apellido} - Tel: {telefono}"
                    except Exception:
                        # Si falla la consulta, continuamos con cliente no registrado
                        pass
                
                # MÉTODO 1: Obtener productos de la venta a través de la relación pedido-producto_pedido
                productos_encontrados = False
                try:
                    cursor.execute("""
                        SELECT 
                            p.id_producto,
                            p.nombre, 
                            p.categoria, 
                            p.precio, 
                            pp.cantidad, 
                            (p.precio * pp.cantidad) as subtotal,
                            p.descripcion,
                            p.costo
                        FROM pedido ped
                        JOIN producto_pedido pp ON ped.id_pedido = pp.id_pedido
                        JOIN producto p ON pp.id_producto = p.id_producto
                        WHERE ped.id_venta = %s
                    """, (id_venta,))
                    
                    productos = cursor.fetchall()
                    if productos:
                        for producto in productos:
                            id_producto, nombre, categoria, precio, cantidad, subtotal, descripcion, costo = producto
                            costo = costo if costo else 0
                            
                            # Asegurarse de que el nombre no esté vacío
                            if not nombre or nombre.strip() == '':
                                # Intentar obtener el nombre desde otra consulta
                                cursor.execute("SELECT nombre FROM producto WHERE id_producto = %s", (id_producto,))
                                nombre_result = cursor.fetchone()
                                nombre = nombre_result[0] if nombre_result else f"Producto #{id_producto}"
                            
                            info_venta['productos'].append({
                                'nombre': nombre,
                                'categoria': categoria if categoria else "Sin categoría",
                                'precio_unitario': float(precio) if precio else 0,
                                'cantidad': cantidad,
                                'subtotal': float(subtotal) if subtotal else 0,
                                'descripcion': descripcion,
                                'costo': float(costo) if costo else 0,
                                'ganancia': (float(precio) - float(costo)) * cantidad if precio and costo else 0
                            })
                        productos_encontrados = True
                        print(f"✓ Método 1 exitoso: Se encontraron {len(productos)} productos para la venta #{id_venta}")
                except Exception as e:
                    print(f"✗ Error en método 1 para venta #{id_venta}: {str(e)}")
                
                # MÉTODO 6 (NUEVO): Buscar productos en cualquier tabla que pueda estar relacionada con ventas
                if not productos_encontrados:
                    try:
                        # Buscar todas las tablas que puedan contener 'producto' en su nombre
                        cursor.execute("SHOW TABLES LIKE '%producto%'")
                        tablas_producto = [t[0] for t in cursor.fetchall()]
                        
                        # Buscar todas las tablas que puedan contener 'venta' en su nombre
                        cursor.execute("SHOW TABLES LIKE '%venta%'")
                        tablas_venta = [t[0] for t in cursor.fetchall()]
                        
                        print(f"Tablas relacionadas con productos: {tablas_producto}")
                        print(f"Tablas relacionadas con ventas: {tablas_venta}")
                        
                        # Verificar si existe una tabla de detalles de venta
                        for tabla in tablas_existentes:
                            if 'detalle' in tabla.lower() and ('venta' in tabla.lower() or 'orden' in tabla.lower()):
                                try:
                                    # Determinar qué columnas tiene esta tabla
                                    cursor.execute(f"DESCRIBE {tabla}")
                                    columnas = [col[0].lower() for col in cursor.fetchall()]
                                    
                                    # Buscar columnas que pueden contener ID de venta e ID de producto
                                    col_venta = next((col for col in columnas if 'venta' in col and 'id' in col), None)
                                    col_producto = next((col for col in columnas if 'producto' in col and 'id' in col), None)
                                    
                                    if col_venta and col_producto:
                                        # Intentar consulta
                                        query = f"""
                                            SELECT 
                                                p.id_producto,
                                                p.nombre, 
                                                p.categoria, 
                                                p.precio, 
                                                d.cantidad, 
                                                p.precio * d.cantidad as subtotal,
                                                p.descripcion,
                                                p.costo
                                            FROM {tabla} d
                                            JOIN producto p ON d.{col_producto} = p.id_producto
                                            WHERE d.{col_venta} = %s
                                        """
                                        cursor.execute(query, (id_venta,))
                                        productos = cursor.fetchall()
                                        
                                        if productos:
                                            for producto in productos:
                                                id_producto, nombre, categoria, precio, cantidad, subtotal, descripcion, costo = producto
                                                costo = costo if costo else 0
                                                
                                                info_venta['productos'].append({
                                                    'nombre': nombre if nombre else f"Producto #{id_producto}",
                                                    'categoria': categoria if categoria else "Sin categoría",
                                                    'precio_unitario': float(precio) if precio else 0,
                                                    'cantidad': cantidad if cantidad else 1,
                                                    'subtotal': float(subtotal) if subtotal else 0,
                                                    'descripcion': descripcion,
                                                    'costo': float(costo) if costo else 0,
                                                    'ganancia': (float(precio) - float(costo)) * cantidad if precio and costo else 0
                                                })
                                            productos_encontrados = True
                                            print(f"✓ Método 6 exitoso: Se encontraron {len(productos)} productos para la venta #{id_venta} en tabla {tabla}")
                                            break
                                except Exception as e:
                                    print(f"✗ Error al intentar con tabla {tabla}: {str(e)}")
                                    
                        # Si no se encontró nada, intentar otra estrategia: ventas_productos si existe
                        if not productos_encontrados and 'ventas_productos' in tablas_existentes:
                            try:
                                cursor.execute("""
                                    SELECT 
                                        p.id_producto,
                                        p.nombre, 
                                        p.categoria, 
                                        p.precio, 
                                        vp.cantidad, 
                                        p.precio * vp.cantidad as subtotal,
                                        p.descripcion,
                                        p.costo
                                    FROM ventas_productos vp
                                    JOIN producto p ON vp.id_producto = p.id_producto
                                    WHERE vp.id_venta = %s
                                """, (id_venta,))
                                
                                productos = cursor.fetchall()
                                if productos:
                                    for producto in productos:
                                        id_producto, nombre, categoria, precio, cantidad, subtotal, descripcion, costo = producto
                                        costo = costo if costo else 0
                                        
                                        info_venta['productos'].append({
                                            'nombre': nombre if nombre else f"Producto #{id_producto}",
                                            'categoria': categoria if categoria else "Sin categoría",
                                            'precio_unitario': float(precio) if precio else 0,
                                            'cantidad': cantidad if cantidad else 1,
                                            'subtotal': float(subtotal) if subtotal else 0,
                                            'descripcion': descripcion,
                                            'costo': float(costo) if costo else 0,
                                            'ganancia': (float(precio) - float(costo)) * cantidad if precio and costo else 0
                                        })
                                    productos_encontrados = True
                                    print(f"✓ Método 6 exitoso: Se encontraron {len(productos)} productos para la venta #{id_venta} en ventas_productos")
                            except Exception as e:
                                print(f"✗ Error al intentar con ventas_productos: {str(e)}")
                    except Exception as e:
                        print(f"✗ Error en método 6 para venta #{id_venta}: {str(e)}")
                
                # MÉTODO 7 (NUEVO): Intentar recuperar el producto asociado a través de cualquier identificador en ventas
                if not productos_encontrados:
                    try:
                        # Obtener todas las columnas de la tabla ventas
                        cursor.execute("DESCRIBE ventas")
                        columnas_ventas = cursor.fetchall()
                        
                        # Buscar cualquier columna que pueda contener un ID de producto
                        columnas_producto = [col[0] for col in columnas_ventas if 'producto' in col[0].lower()]
                        
                        if columnas_producto:
                            for col_prod in columnas_producto:
                                try:
                                    # Intentar obtener el ID del producto
                                    cursor.execute(f"""
                                        SELECT {col_prod}
                                        FROM ventas 
                                        WHERE id_venta = %s
                                    """, (id_venta,))
                                    
                                    id_producto_result = cursor.fetchone()
                                    
                                    if id_producto_result and id_producto_result[0]:
                                        id_producto = id_producto_result[0]
                                        
                                        # Obtener detalles del producto
                                        cursor.execute("""
                                            SELECT id_producto, nombre, categoria, precio, descripcion, costo
                                            FROM producto
                                            WHERE id_producto = %s
                                        """, (id_producto,))
                                        
                                        producto_info = cursor.fetchone()
                                        
                                        if producto_info:
                                            id_prod, nombre, categoria, precio, descripcion, costo = producto_info
                                            costo = costo if costo else 0
                                            
                                            info_venta['productos'].append({
                                                'nombre': nombre if nombre else f"Producto #{id_producto}",
                                                'categoria': categoria if categoria else "Sin categoría",
                                                'precio_unitario': float(precio) if precio else 0,
                                                'cantidad': 1,
                                                'subtotal': float(precio) if precio else float(total_venta) if total_venta else 0,
                                                'descripcion': descripcion,
                                                'costo': float(costo) if costo else 0,
                                                'ganancia': (float(precio) - float(costo)) if precio and costo else 0
                                            })
                                            productos_encontrados = True
                                            print(f"✓ Método 7 exitoso: Se encontró producto con ID {id_producto} para la venta #{id_venta} mediante columna {col_prod}")
                                            break
                                except Exception as e:
                                    print(f"✗ Error al intentar recuperar producto usando columna {col_prod}: {str(e)}")
                    except Exception as e:
                        print(f"✗ Error en método 7 para venta #{id_venta}: {str(e)}")
                
                # MÉTODO 8 (NUEVO): Intentar recuperar directamente nombres de productos mediante búsqueda en texto de venta
                if not productos_encontrados:
                    try:
                        # Verificar si hay alguna columna que pueda contener nombres o descripciones de productos
                        cursor.execute("DESCRIBE ventas")
                        columnas_ventas = cursor.fetchall()
                        
                        posibles_columnas_descripcion = [
                            col[0] for col in columnas_ventas 
                            if any(nombre in col[0].lower() for nombre in ['detalle', 'descripcion', 'texto', 'nombre', 'concepto'])
                        ]
                        
                        if posibles_columnas_descripcion:
                            for col_desc in posibles_columnas_descripcion:
                                try:
                                    # Obtener el texto descriptivo
                                    cursor.execute(f"""
                                        SELECT {col_desc}
                                        FROM ventas 
                                        WHERE id_venta = %s
                                    """, (id_venta,))
                                    
                                    descripcion_result = cursor.fetchone()
                                    
                                    if descripcion_result and descripcion_result[0]:
                                        texto_venta = descripcion_result[0]
                                        
                                        # Obtener todos los productos para buscar coincidencias
                                        cursor.execute("SELECT id_producto, nombre, categoria, precio, costo FROM producto")
                                        todos_productos = cursor.fetchall()
                                        
                                        productos_encontrados_texto = []
                                        
                                        # Buscar productos que coincidan en el texto
                                        for prod in todos_productos:
                                            id_prod, nombre_prod, categoria, precio, costo = prod
                                            if nombre_prod and nombre_prod.lower() in texto_venta.lower():
                                                productos_encontrados_texto.append(prod)
                                        
                                        if productos_encontrados_texto:
                                            for prod in productos_encontrados_texto:
                                                id_prod, nombre, categoria, precio, costo = prod
                                                costo = costo if costo else 0
                                                
                                                info_venta['productos'].append({
                                                    'nombre': nombre,
                                                    'categoria': categoria if categoria else "Sin categoría",
                                                    'precio_unitario': float(precio) if precio else 0,
                                                    'cantidad': 1,  # Asumimos cantidad 1 ya que no tenemos ese dato
                                                    'subtotal': float(precio) if precio else 0,
                                                    'descripcion': texto_venta,
                                                    'costo': float(costo) if costo else 0,
                                                    'ganancia': (float(precio) - float(costo)) if precio and costo else 0
                                                })
                                            
                                            productos_encontrados = True
                                            print(f"✓ Método 8 exitoso: Se encontraron {len(productos_encontrados_texto)} productos en texto para la venta #{id_venta}")
                                            break
                                except Exception as e:
                                    print(f"✗ Error al intentar recuperar productos en texto usando columna {col_desc}: {str(e)}")
                    except Exception as e:
                        print(f"✗ Error en método 8 para venta #{id_venta}: {str(e)}")
                
                # Si después de todos los métodos no se encontraron productos, registrar como venta genérica
                if not productos_encontrados:
                    info_venta['productos'].append({
                        'nombre': f"Venta #{id_venta}",
                        'categoria': "Sin categoría",
                        'precio_unitario': float(total_venta) if total_venta else 0,
                        'cantidad': 1,
                        'subtotal': float(total_venta) if total_venta else 0,
                        'descripcion': "Detalles no disponibles",
                        'costo': 0,
                        'ganancia': float(total_venta) if total_venta else 0
                    })
                    print(f"! Método 5 (fallback): No se pudieron encontrar productos para la venta #{id_venta}")
                
                # Agregar la información completa de esta venta
                ventas_detalladas.append(info_venta)
            
            cursor.close()
            conexion.close()
            
            if not ventas_detalladas:
                raise Exception("No se pudieron obtener los detalles de las ventas del día")
            
            # Preparar nombre del archivo
            nombre_archivo = f"reporte_detallado_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Diálogo para guardar archivo
            ruta_guardar = QFileDialog.getSaveFileName(
                self,
                "Guardar reporte detallado de ventas",
                nombre_archivo,
                "PDF files (*.pdf)"
            )[0]
            
            if ruta_guardar:
                # Crear documento PDF
                doc = SimpleDocTemplate(ruta_guardar, pagesize=landscape(letter))
                elements = []
                
                # Estilos
                styles = getSampleStyleSheet()
                title_style = styles["Title"]
                subtitle_style = ParagraphStyle(
                    'Subtitle', 
                    parent=styles['Heading2'],
                    alignment=1,  # Centered
                    spaceAfter=12
                )
                heading_style = ParagraphStyle(
                    'Heading', 
                    parent=styles['Heading3'],
                    spaceBefore=15,
                    spaceAfter=10
                )
                normal_style = styles["Normal"]
                
                # Título principal
                elements.append(Paragraph("REPORTE DETALLADO DE VENTAS DIARIAS", title_style))
                elements.append(Spacer(1, 10))
                
                # Información de fecha
                fecha_info = f"{dia_semana}, {fecha_actual} - Generado a las {hora_actual}"
                elements.append(Paragraph(fecha_info, subtitle_style))
                elements.append(Spacer(1, 20))
                
                # Resumen general
                elements.append(Paragraph("RESUMEN GENERAL", heading_style))
                
                # Tabla de resumen
                resumen_data = [['TOTAL VENTAS', 'PRODUCTOS VENDIDOS', 'GANANCIA TOTAL']]
                
                # Calcular totales
                total_productos = sum(sum(p['cantidad'] for p in v['productos']) for v in ventas_detalladas)
                total_ganancia = sum(sum(p['ganancia'] for p in v['productos']) for v in ventas_detalladas)
                
                resumen_data.append([
                    f"${importe_total_dia:.2f}",
                    str(total_productos),
                    f"${total_ganancia:.2f}"
                ])
                
                # Crear tabla de resumen
                resumen_table = Table(resumen_data, colWidths=[200, 200, 200])
                resumen_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
                ]))
                
                elements.append(resumen_table)
                elements.append(Spacer(1, 30))
                
                # Detalle por venta
                elements.append(Paragraph("DETALLE DE VENTAS INDIVIDUALES", heading_style))
                
                # Para cada venta, crear una sección
                for i, venta in enumerate(ventas_detalladas):
                    # Título de la venta con más detalle
                    elements.append(Paragraph(f"VENTA #{venta['id_venta']} - {venta['fecha']}", heading_style))
                    
                    # Información del cliente con estilo destacado
                    cliente_style = ParagraphStyle(
                        'Cliente', 
                        parent=styles['Normal'],
                        fontSize=11,
                        textColor=colors.navy,
                        spaceBefore=5,
                        spaceAfter=5
                    )
                    elements.append(Paragraph(f"<b>Cliente:</b> {venta['cliente']}", cliente_style))
                    elements.append(Spacer(1, 5))
                    
                    # Subtítulo para la lista de productos
                    productos_title_style = ParagraphStyle(
                        'ProductosTitle', 
                        parent=styles['Normal'],
                        fontSize=12,
                        textColor=colors.darkorange,
                        spaceBefore=5,
                        spaceAfter=5,
                        leading=14
                    )
                    elements.append(Paragraph("<b>DETALLE DE PRODUCTOS VENDIDOS:</b>", productos_title_style))
                    elements.append(Spacer(1, 5))
                    
                    # Tabla de productos de esta venta con diseño mejorado
                    productos_data = [['PRODUCTO', 'CATEGORÍA', 'PRECIO UNIT.', 'CANTIDAD', 'SUBTOTAL', 'COSTO UNIT.', 'GANANCIA']]
                    
                    # Total de esta venta
                    venta_total_productos = 0
                    venta_total_items = 0
                    
                    for producto in venta['productos']:
                        productos_data.append([
                            producto['nombre'],
                            producto['categoria'],
                            f"${producto['precio_unitario']:.2f}",
                            str(int(producto['cantidad'])) if isinstance(producto['cantidad'], (int, float)) else producto['cantidad'],
                            f"${producto['subtotal']:.2f}",
                            f"${producto['costo']:.2f}",
                            f"${producto['ganancia']:.2f}"
                        ])
                        # Acumular totales para esta venta
                        venta_total_productos += 1
                        venta_total_items += float(producto['cantidad']) if isinstance(producto['cantidad'], (int, float)) else 1
                    
                    # Fila del total de esta venta con más información
                    productos_data.append(['', '', '', 'TOTAL:', f"${venta['total']:.2f}", '', ''])
                    
                    # Crear tabla de productos con estilo mejorado
                    productos_table = Table(productos_data, colWidths=[120, 80, 70, 55, 70, 70, 70])
                    productos_table.setStyle(TableStyle([
                        # Encabezados
                        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        
                        # Contenido
                        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
                        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
                        ('ALIGN', (2, 1), (6, -2), 'RIGHT'),  # Alinear valores numéricos a la derecha
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        
                        # Fila del total
                        ('SPAN', (0, -1), (2, -1)),  # Combinar celdas para el total
                        ('BACKGROUND', (3, -1), (4, -1), colors.darkblue),
                        ('TEXTCOLOR', (3, -1), (4, -1), colors.whitesmoke),
                        ('FONTNAME', (3, -1), (4, -1), 'Helvetica-Bold'),
                        ('ALIGN', (3, -1), (4, -1), 'RIGHT'),
                        ('BOX', (3, -1), (4, -1), 1, colors.black),
                    ]))
                    
                    elements.append(productos_table)
                    
                    # Añadir resumen de productos de esta venta
                    resumen_venta_style = ParagraphStyle(
                        'ResumenVenta', 
                        parent=styles['Normal'],
                        fontSize=10,
                        textColor=colors.darkblue,
                        spaceBefore=8,
                        spaceAfter=8
                    )
                    
                    elements.append(Spacer(1, 8))
                    elements.append(Paragraph(
                        f"<b>Resumen de venta:</b> {venta_total_productos} productos diferentes, {int(venta_total_items)} items en total", 
                        resumen_venta_style
                    ))
                
                # Generar PDF
                doc.build(elements)
                
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Reporte detallado de ventas exportado exitosamente a:\n{ruta_guardar}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar reporte de ventas diarias:\n{str(e)}"
            )
        
        # DIAGNÓSTICO: Comprobar estructura de tablas y datos
        print("=== DIAGNÓSTICO DE BASE DE DATOS ===")
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tablas_existentes = [t[0] for t in cursor.fetchall()]
        print(f"Tablas existentes: {tablas_existentes}")
        
        # Verificar si hay productos en la tabla
        if 'producto' in tablas_existentes:
            cursor.execute("SELECT COUNT(*) FROM producto")
            total_productos = cursor.fetchone()[0]
            print(f"Total de productos en la base de datos: {total_productos}")
            
            # Mostrar algunos ejemplos de productos
            cursor.execute("SELECT id_producto, nombre, categoria, precio FROM producto LIMIT 5")
            ejemplos = cursor.fetchall()
            print("Ejemplos de productos:")
            for ejemplo in ejemplos:
                print(f"  ID: {ejemplo[0]}, Nombre: {ejemplo[1]}, Categoría: {ejemplo[2]}, Precio: {ejemplo[3]}")
        
        # Verificar ventas del día
        cursor.execute("SELECT COUNT(*) FROM ventas WHERE DATE(fecha) = CURDATE()")
        total_ventas = cursor.fetchone()[0]
        print(f"Total de ventas hoy: {total_ventas}")
        
        # Intentar determinar la estructura de relaciones
        for tabla in ['ventas', 'pedido', 'producto_pedido']:
            if tabla in tablas_existentes:
                cursor.execute(f"DESCRIBE {tabla}")
                columnas = cursor.fetchall()
                columnas_nombres = [col[0] for col in columnas]
                print(f"Columnas en {tabla}: {columnas_nombres}")
                


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainAjustes()
    window.show()
    sys.exit(app.exec())
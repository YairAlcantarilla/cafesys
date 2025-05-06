import sys
import Caja, P_Registros, personal, login, p_inventario, main_p, P_Ajustes
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QDialog, QMessageBox
)
from conexion import conectar_db
from datetime import datetime, timedelta
import json
import os
from win10toast import ToastNotifier

class MainR(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registros del Sistema")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Mregistros.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
        ###########################################
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
        ######################################################

    
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


        # Tabla de registros
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 1000, 555)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels([
            "ID Reporte", "Tipo de Reporte", "Periodo", "Datos"
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

        # Configurar columnas con nuevo ajuste
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        # Habilitar ajuste de texto
        self.table_widget.setWordWrap(True)

        # Cargar datos
        self.cargar_datos()

        # Botón de regresar
        self.regresar_button = QPushButton("Regresar", self) 
        self.regresar_button.setGeometry(1270, 655, 77, 70)
        self.regresar_button.setStyleSheet("""
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
        self.regresar_button.clicked.connect(self.regresar)

        # Añadir botón para generar reporte
        self.generar_reporte_button = QPushButton("Generar Reporte", self)
        self.generar_reporte_button.setGeometry(1180, 150, 150, 70)
        self.generar_reporte_button.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
        """)
        self.generar_reporte_button.clicked.connect(self.generar_reporte_venta)

        # Añadir botón para ver ventas
        self.ver_ventas_button = QPushButton("Ver Ventas", self)
        self.ver_ventas_button.setGeometry(1180, 250, 150, 70)
        self.ver_ventas_button.setStyleSheet("""
            QPushButton {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
            }
            QPushButton:hover {
                background-color: rgba(230, 170, 104, 0.2);
            }
        """)
        self.ver_ventas_button.clicked.connect(self.mostrar_ventas)

        # Configurar timer para verificar la hora
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.timer.start(60000)  # Verificar cada minuto
        
        # Añadir estas variables para controlar el tiempo
        self.ultimo_reporte = None
        self.intervalo_minimo = None
        self.load_configured_time()

        # Crear el notificador
        self.toaster = ToastNotifier()

    def load_configured_time(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.configured_time = config.get('scheduled_time', '23:59')
                    # Calcular el intervalo hasta la próxima hora programada
                    self.actualizar_intervalo()
            else:
                self.configured_time = '23:59'
                self.intervalo_minimo = timedelta(hours=24)
        except Exception as e:
            print(f"Error cargando hora configurada: {e}")
            self.configured_time = '23:59'
            self.intervalo_minimo = timedelta(hours=24)

    def actualizar_intervalo(self):
        """Calcula el tiempo hasta la próxima hora programada"""
        now = datetime.now()
        scheduled_hour, scheduled_minute = map(int, self.configured_time.split(':'))
        next_run = now.replace(hour=scheduled_hour, minute=scheduled_minute)
        
        if next_run <= now:
            next_run += timedelta(days=1)
        
        self.intervalo_minimo = next_run - now

    def check_time(self):
        current_time = datetime.now().strftime('%H:%M')
        if current_time == self.configured_time:
            self.generar_reporte_automatico()

    def generar_reporte_automatico(self):
        try:
            # Generar reporte automático
            self.generar_reporte_venta()
            
            # Actualizar el tiempo del último reporte
            self.ultimo_reporte = datetime.now()
            self.actualizar_intervalo()
            
            # Reemplazar QMessageBox con notificación de Windows
            self.toaster.show_toast(
                "CAFESYS - Reporte Automático",
                f"Se ha generado un reporte automático programado para las {self.configured_time}",
                icon_path="imagenes/CAFESYSNUEVO.png",
                duration=5,
                threaded=True
            )
        except Exception as e:
            print(f"Error generando reporte automático: {e}")
            self.toaster.show_toast(
                "CAFESYS - Error",
                f"Error al generar reporte automático: {str(e)}",
                icon_path="imagenes/CAFESYSNUEVO.png",
                duration=5,
                threaded=True
            )

    def cargar_datos(self):
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            consulta = """
                SELECT ID_reporte, TipoReporte, Periodo, datos 
                FROM reporte 
                ORDER BY ID_reporte DESC
            """
            cursor.execute(consulta)
            registros = cursor.fetchall()
            
            self.table_widget.setRowCount(len(registros))
            
            for fila, registro in enumerate(registros):
                for columna, valor in enumerate(registro):
                    item = QTableWidgetItem(str(valor))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table_widget.setItem(fila, columna, item)
                    
                    # Ajustar altura de la fila según el contenido
                    if columna == 3:  # Columna de Datos
                        self.table_widget.resizeRowToContents(fila)
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def generar_reporte_venta(self):
        try:
            # Verificar si ha pasado suficiente tiempo desde el último reporte
            if self.ultimo_reporte is not None:
                tiempo_transcurrido = datetime.now() - self.ultimo_reporte
                tiempo_restante = self.intervalo_minimo - tiempo_transcurrido
                
                if tiempo_transcurrido < self.intervalo_minimo:
                    horas = int(tiempo_restante.total_seconds() // 3600)
                    minutos = int((tiempo_restante.total_seconds() % 3600) // 60)
                    QMessageBox.warning(
                        self,
                        "Espera Requerida",
                        f"Debe esperar {horas} horas y {minutos} minutos para generar otro reporte manual.\n"
                        f"Próximo reporte programado: {self.configured_time}"
                    )
                    return

            conexion = conectar_db()
            cursor = conexion.cursor()
            
            # Obtener la fecha actual
            fecha_actual = datetime.now().date()
            
            # Obtener las ventas solo del día actual
            cursor.execute("""
                SELECT producto, cantidad, precio_total, forma_pago 
                FROM ventas 
                WHERE DATE(fecha) = %s
            """, (fecha_actual,))
            ventas = cursor.fetchall()
            
            if not ventas:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"No hay ventas registradas para el día de hoy ({fecha_actual})"
                )
                return
            
            # Procesar datos para el reporte
            total_ventas = sum(venta[1] for venta in ventas)
            total_dinero = sum(venta[2] for venta in ventas)
            metodos_pago = list(set(venta[3] for venta in ventas))
            productos = [f"{venta[0]}(x{venta[1]})" for venta in ventas]
            
            # Crear mensaje del reporte
            datos_reporte = (
                f"El dia de hoy {fecha_actual} se vendieron {total_ventas} productos "
                f"({', '.join(productos)}) con un costo total de ${total_dinero:.2f} "
                f"usando los metodos de pago {', '.join(metodos_pago)}"
            )
            
            # Insertar el reporte en la base de datos
            cursor.execute("""
                INSERT INTO reporte (TipoReporte, Periodo, datos)
                VALUES (%s, %s, %s)
            """, ('Venta', fecha_actual, datos_reporte))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            # Actualizar el tiempo del último reporte
            self.ultimo_reporte = datetime.now()
            self.actualizar_intervalo()
            
            # Recargar la tabla
            self.cargar_datos()
            
            # Reemplazar QMessageBox con notificación de Windows
            self.toaster.show_toast(
                "CAFESYS - Reporte Generado",
                "El reporte de ventas ha sido generado correctamente",
                icon_path="imagenes/CAFESYSNUEVO.png",  # Ruta al ícono de tu app
                duration=5,  # Duración en segundos
                threaded=True  # Permite que la app siga funcionando durante la notificación
            )
            
        except Exception as e:
            self.toaster.show_toast(
                "CAFESYS - Error",
                f"Error al generar reporte: {str(e)}",
                icon_path="imagenes/CAFESYSNUEVO.png",
                duration=5,
                threaded=True
            )

    def mostrar_ventas(self):
        ventas_window = VentasWindow(self)
        ventas_window.exec()

    def regresar(self):
        from p_inicio import MainWindow
        self.cambioP = MainWindow()
        self.cambioP.show()
        self.close()

    def button_clicked(self):
        button = self.sender()
        
        if button.text() == "Caja":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de Registros?",
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
                "¿Está seguro de que desea salir de Registros?",
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
                "¿Está seguro de que desea salir de Registros?",
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
                "¿Está seguro de que desea salir de Registros?",
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
                "¿Está seguro de que desea salir de Registros?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = p_inventario.MainWindow()
                self.main_window.show()
                self.close()
        elif button.text() == "Ajustes":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de Registros?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.main_window = P_Ajustes.MainAjustes()
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
####        

class VentasWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tabla de Ventas")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #0D1321;")

        # Layout principal
        layout = QVBoxLayout(self)

        # Tabla de ventas
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels([
            "ID Venta", "Producto", "Fecha", "Cantidad", 
            "Precio Total", "Forma de Pago"
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

        # Configurar columnas
        header = self.table_widget.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table_widget)

        # Cargar datos
        self.cargar_ventas()

    def cargar_ventas(self):
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            fecha_actual = datetime.now().date()
            
            consulta = """
                SELECT id_venta, producto, fecha, cantidad, 
                       precio_total, forma_pago 
                FROM ventas 
                WHERE DATE(fecha) = %s
                ORDER BY fecha DESC, id_venta DESC
            """
            cursor.execute(consulta, (fecha_actual,))
            ventas = cursor.fetchall()
            
            self.table_widget.setRowCount(len(ventas))
            
            for fila, venta in enumerate(ventas):
                for columna, valor in enumerate(venta):
                    if columna == 4:  # Formato para precio
                        texto = f"${valor:.2f}"
                    else:
                        texto = str(valor)
                    
                    item = QTableWidgetItem(texto)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table_widget.setItem(fila, columna, item)
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar ventas: {str(e)}")


######################################
        
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainR()
    window.show()
    sys.exit(app.exec())

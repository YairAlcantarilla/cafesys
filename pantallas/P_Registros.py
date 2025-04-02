import sys
import Caja, P_Registros, personal, login, p_inventario, main_p, P_Ajustes
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QDialog, QMessageBox
)
from conexion import conectar_db

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
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            # Obtener la fecha más reciente
            cursor.execute("SELECT DISTINCT fecha FROM ventas ORDER BY fecha DESC LIMIT 1")
            fecha_reporte = cursor.fetchone()[0]
            
            # Obtener todas las ventas del día
            cursor.execute("""
                SELECT producto, cantidad, precio_total, forma_pago 
                FROM ventas 
                WHERE fecha = %s
            """, (fecha_reporte,))
            ventas = cursor.fetchall()
            
            if not ventas:
                raise Exception(f"No hay ventas registradas para la fecha {fecha_reporte}")
            
            # Procesar datos para el reporte
            total_ventas = sum(venta[1] for venta in ventas)  # Suma de cantidades
            total_dinero = sum(venta[2] for venta in ventas)  # Suma de precio_total
            metodos_pago = list(set(venta[3] for venta in ventas))  # Métodos de pago únicos
            productos = [f"{venta[0]}(x{venta[1]})" for venta in ventas]  # Productos con cantidades
            
            # Crear mensaje del reporte
            datos_reporte = (
                f"El dia de hoy {fecha_reporte} se vendieron {total_ventas} productos "
                f"({', '.join(productos)}) con un costo total de ${total_dinero:.2f} "
                f"usando los metodos de pago {', '.join(metodos_pago)}"
            )
            
            # Insertar el reporte en la base de datos
            cursor.execute("""
                INSERT INTO reporte (TipoReporte, Periodo, datos)
                VALUES (%s, %s, %s)
            """, ('Venta', fecha_reporte, datos_reporte))
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            # Recargar la tabla
            self.cargar_datos()
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al generar reporte: {str(e)}")

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
            
            consulta = """
                SELECT id_venta, producto, fecha, cantidad, 
                       precio_total, forma_pago 
                FROM ventas 
                ORDER BY fecha DESC, id_venta DESC
            """
            cursor.execute(consulta)
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
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al cargar ventas: {str(e)}")


######################################
        
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainR()
    window.show()
    sys.exit(app.exec())

import sys
import p_inicio
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
            # Aquí puedes agregar la lógica para usar el tiempo seleccionado
            QMessageBox.information(
                self,
                "Hora Configurada",
                f"Hora establecida: {selected_time}"
            )
            # Guardar el tiempo seleccionado como atributo de la clase
            self.configured_time = selected_time
            
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
            # Configuración de la base de datos
            DB_NAME = "tienda"
            DB_USER = "root"
            DB_PASS = "894388"
            DB_HOST = "localhost"

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

                # Ejecutar el comando
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
            # Configuración de la base de datos
            DB_NAME = "tienda"
            DB_USER = "root"
            DB_PASS = "894388"
            DB_HOST = "localhost"

            # Abrir diálogo para seleccionar archivo
            ruta_archivo = QFileDialog.getOpenFileName(
                self,
                "Seleccionar archivo de respaldo",
                "",
                "SQL files (*.sql)"
            )[0]

            if ruta_archivo:
                # Verificar que el archivo existe
                if not os.path.exists(ruta_archivo):
                    raise Exception("El archivo seleccionado no existe")

                # Comando para restaurar la base de datos
                comando = f'mysql -h {DB_HOST} -u {DB_USER}'
                if DB_PASS:
                    comando += f' -p{DB_PASS}'
                comando += f' {DB_NAME} < "{ruta_archivo}"'

                # Ejecutar el comando
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

            # Obtener datos de la tabla reportes
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT ID_reporte, TipoReporte, Periodo, datos 
                FROM reporte 
                ORDER BY ID_reporte DESC
            """)
            
            reportes = cursor.fetchall()
            cursor.close()
            conexion.close()

            if not reportes:
                raise Exception("No hay reportes para exportar")

            # Crear DataFrame
            df = pd.DataFrame(
                reportes,
                columns=['ID Reporte', 'Tipo de Reporte', 'Periodo', 'Datos']
            )

            # Obtener ubicación para guardar
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reportes_{fecha_actual}.xlsx"
            
            ruta_guardar = QFileDialog.getSaveFileName(
                self,
                "Guardar reportes",
                nombre_archivo,
                "Excel files (*.xlsx)"
            )[0]

            if ruta_guardar:
                # Exportar a Excel
                df.to_excel(
                    ruta_guardar,
                    index=False,
                    sheet_name='Reportes'
                )

                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Reportes exportados exitosamente a:\n{ruta_guardar}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar reportes:\n{str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainAjustes()
    window.show()
    sys.exit(app.exec())
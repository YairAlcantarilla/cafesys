import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, 
    QWidget, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView
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

        # Configurar columnas
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

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

    def cargar_datos(self):
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            
            consulta = """
                SELECT ID_reporte, TipoReporte, Periodo, datos 
                FROM reportes 
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
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def regresar(self):
        from p_inicio import MainWindow
        self.cambioP = MainWindow()
        self.cambioP.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainR()
    window.show()
    sys.exit(app.exec())

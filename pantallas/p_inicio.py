import p_producto
import Caja
import personal
import main_p
import p_inventario
import P_Registros, P_Ajustes
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/fondomenu1.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        button_configs = [
            ["Caja", 94, 186, 222, 394],
            ["Reportes", 334, 186, 222, 394],
            ["Productos", 573, 186, 222, 394],
            ["Personal", 811, 186, 222, 394],
            ["Inventario",1050, 186, 222, 394],
            ["Ajustes", 1152, 10, 90, 90],
            ["Salir", 1268, 10, 70, 90],
            ["Ayuda", 1248, 705, 102, 45],
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
                background-color: rgba(255, 255, 255, 25);
            }
            QPushButton:pressed {
                background-color: rgba(230, 170, 104, 70);
            }
        """)

            self.buttons.append(button)
        
        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Productos":
            self.main_window = main_p.MainPWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "Caja":
            self.main_window = Caja.CajaI()
            self.main_window.show()
            self.close()
        elif button.text() == "Personal":
            self.main_window = personal.MainPersonal()
            self.main_window.show()
            self.close()
        elif button.text() == "Inventario":
            self.main_window = p_inventario.MainWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "Reportes":
            self.main_window = P_Registros.MainR()
            self.main_window.show()
            self.close()
        elif button.text() == "Ajustes":
            self.main_window = P_Ajustes.MainAjustes()
            self.main_window.show()
            self.close()
        elif button.text() == "Salir":
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

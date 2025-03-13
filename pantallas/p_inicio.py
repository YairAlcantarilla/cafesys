import p_producto
import Caja
import personal
import main_p
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
        pixmap = QPixmap('imagenes/fondomenu.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        button_configs = [
            ["Caja", 30, 152, 200, 50],
            ["Reportes", 30, 227, 200, 50],
            ["Productos", 30, 303, 200, 50],
            ["Personal", 30, 378, 200, 50],
            ["Inventario", 30, 454, 200, 50],
            ["Ajustes", 30, 530, 200, 50],
            ["Salir", 30, 605, 200, 50]
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
        if button.text() == "Productos":
            self.main_window = main_p.MainPWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "Caja":
            self.main_window = Caja.MainCaja()
            self.main_window.show()
            self.close()
        elif button.text() == "Personal":
            self.main_window = personal.MainPersonal()
            self.main_window.show()
            self.close()
        elif button.text() == "Salir":
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

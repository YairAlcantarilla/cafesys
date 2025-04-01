import p_producto
import p_inicio
import p_combo
import p_desc
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

class MainPWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/menup.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # aca van los botones w
        # para ajustar es cord x, cord y, y ancho y alto
        button_configs = [
            ["Sproducto", 333, 187, 222, 394],
            ["Scombo", 573, 187, 222, 394],
            ["Sdesc", 812, 187, 222, 394],
            ["Regresar", 1268, 10, 70, 90],
            
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
                background-color: rgba(255, 255, 255, 30);
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
        if button.text() == "Sproducto":
            self.main_window = p_producto.MainWindow()
            self.main_window.show()
            self.close()
        elif button.text() == "Regresar":
            self.main_window = p_inicio.MainWindow()  
            self.main_window.show()
            self.close()
        elif button.text() == "Scombo":
            self.main_window = p_combo.MainCombo()  
            self.main_window.show()
            self.close()
        elif button.text() == "Sdesc":
            self.main_window = p_desc.MainDesc()  
            self.main_window.show()
            self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPWindow()
    window.show()
    sys.exit(app.exec())

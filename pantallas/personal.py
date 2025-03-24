import p_inicio
import sys
import conexion
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QGraphicsOpacityEffect, QLineEdit,
                           QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                           QRadioButton, QButtonGroup)
#################################### Interfaz principal de personal #######################################################

class MainPersonal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # fondo
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Mpersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)  # x, y, width, height
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels([
            "ID", "Contraseña", "Nombre", "Teléfono", "Dirección", "ID Puesto"
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

        # Ajustar el ancho de las columnas
        header = self.table_widget.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Cargar datos
        self.cargar_datos()

        button_configs = [
            #otrosbotones
            ["AgregarE", 875, 144, 344, 55],
            ["EliminarE", 875, 225, 344, 55],
            ["EditarE", 875, 306, 344, 55],
            ["RegresarE", 1270, 655, 77, 70],
            
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 50);
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

    def cargar_datos(self):
        try:
            from conexion import mostrar_usuarios
            usuarios = mostrar_usuarios()
            
            self.table_widget.setRowCount(len(usuarios))
            
            for fila, usuario in enumerate(usuarios):
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(usuario[0])))  # ID
                self.table_widget.setItem(fila, 1, QTableWidgetItem('*****'))          # Contraseña oculta
                self.table_widget.setItem(fila, 2, QTableWidgetItem(str(usuario[2])))  # Nombre
                self.table_widget.setItem(fila, 3, QTableWidgetItem(str(usuario[3])))  # Teléfono
                self.table_widget.setItem(fila, 4, QTableWidgetItem(str(usuario[4])))  # Dirección
                self.table_widget.setItem(fila, 5, QTableWidgetItem(str(usuario[5])))  # ID_Puesto
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(f"Error al cargar los usuarios: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()

    def button_clicked(self):
        button = self.sender()
        if button.text() == "AgregarE":
            self.cambioP = AgregarE()
        elif button.text() == "EliminarE":
            self.cambioP = EliminarE()
        elif button.text() == "EditarE":
            self.cambioP = EditarE()
        elif button.text() == "RegresarE":
            self.cambioP = p_inicio.MainWindow()  

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
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()
       

#################################### Interfaz para agregar empleado #######################################################
class AgregarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Apersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Modificar input_configs para quitar el campo de ocupación
        input_configs = [
            ["Nombre", 598, 194, 317, 40],
            ["Direccion", 598, 369, 317, 40],
            ["Telefono", 964, 194, 250, 40], 
            ["Contraseña", 964, 369, 250, 40] 
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
        
        # Crear radio buttons para tipo de usuario
        self.tipo_usuario_group = QButtonGroup(self)
        
        # Radio button para Administrador
        self.admin_radio = QRadioButton("Administrador", self)
        self.admin_radio.move(598, 284)  # Mover a la posición del input eliminado
        self.admin_radio.setStyleSheet("""
            QRadioButton {
                color: #E6AA68;
                font-size: 14px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
                border: 2px solid #E6AA68;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                background-color: #E6AA68;
                border: 2px solid #E6AA68;
            }
        """)
        
        # Radio button para Cajero
        self.cajero_radio = QRadioButton("Cajero", self)
        self.cajero_radio.move(720, 284)  # 30 píxeles debajo del radio de administrador
        self.cajero_radio.setStyleSheet("""
            QRadioButton {
                color: #E6AA68;
                font-size: 14px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
                border: 2px solid #E6AA68;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                background-color: #E6AA68;
                border: 2px solid #E6AA68;
            }
        """)
        
        # Agregar radio buttons al grupo
        self.tipo_usuario_group.addButton(self.admin_radio)
        self.tipo_usuario_group.addButton(self.cajero_radio)

        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
            ["Confirmar", 810, 554, 227, 78],
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

    
    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()     
        elif button.text() == "Confirmar":
            tipo_usuario = 1 if self.admin_radio.isChecked() else 2 if self.cajero_radio.isChecked() else None
            
            if tipo_usuario is None:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un tipo de usuario")
                return

            # Validar teléfono (máximo 10 dígitos)
            telefono = self.inputs[2].text()
            if not telefono.isdigit() or len(telefono) > 10:
                QMessageBox.warning(self, "Advertencia", "El teléfono debe contener solo números y máximo 10 dígitos")
                return
                
            datos = {
                "nombre": self.inputs[0].text(),        # Nombre
                "Direccion": self.inputs[1].text(),     # Dirección
                "telefono": telefono,                   # Teléfono (validado)
                "contrasenna": self.inputs[3].text(),   # Contraseña
                "ID_Puesto": tipo_usuario              # Tipo de usuario (del radio button)
            }

            if all(datos.values()):
                try:
                    conexion.insertar_dato("usuario", datos)
                    QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
        
        self.fade_out()

#################################### Interfaz para eliminar empleado #######################################################
class EliminarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliminar usuario")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Epersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Crear la tabla
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels([
            "ID", "Contraseña", "Nombre", "Teléfono", "Dirección", "ID Puesto"
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

        # Ajustar el ancho de las columnas
        header = self.table_widget.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Cargar datos
        self.cargar_datos()
        
        # Variable para almacenar el ID seleccionado
        self.id_seleccionado = None
        
        # Conectar el evento de selección
        self.table_widget.itemSelectionChanged.connect(self.on_selection_changed)

        button_configs = [
            ["Regresar", 1270, 655, 77, 70],
            ["Confirmar", 810, 554, 227, 78],  # Button for deletion
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

    def cargar_datos(self):
        try:
            from conexion import mostrar_usuarios
            usuarios = mostrar_usuarios()
            
            self.table_widget.setRowCount(len(usuarios))
            
            for fila, usuario in enumerate(usuarios):
                self.table_widget.setItem(fila, 0, QTableWidgetItem(str(usuario[0])))  # ID
                self.table_widget.setItem(fila, 1, QTableWidgetItem('*****'))          # Contraseña oculta
                self.table_widget.setItem(fila, 2, QTableWidgetItem(str(usuario[2])))  # Nombre
                self.table_widget.setItem(fila, 3, QTableWidgetItem(str(usuario[3])))  # Teléfono
                self.table_widget.setItem(fila, 4, QTableWidgetItem(str(usuario[4])))  # Dirección
                self.table_widget.setItem(fila, 5, QTableWidgetItem(str(usuario[5])))  # ID_Puesto
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los usuarios: {str(e)}")

    def on_selection_changed(self):
        selected_items = self.table_widget.selectedItems()
        if selected_items:
            self.id_seleccionado = self.table_widget.item(selected_items[0].row(), 0).text()

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()
            self.fade_out()
        elif button.text() == "Confirmar":
            if self.id_seleccionado:
                reply = QMessageBox.question(self, 'Confirmación', 
                                          '¿Está seguro de eliminar este usuario?',
                                          QMessageBox.StandardButton.Yes | 
                                          QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        from conexion import eliminar_usuario
                        eliminar_usuario(self.id_seleccionado)
                        QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                        self.cambioP = MainPersonal()
                        self.fade_out()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario: {str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un usuario para eliminar")
        
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
   

#################################### Interfaz para Editar empleado #######################################################
class EditarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editar usuario")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EDpersonal .png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
    #**********************************************************************
        button_configs = [
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
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()

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
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()

 #################################### Interfaz para ver lista empleado #######################################################
class ListaE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editar usuario")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Lpersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)
    #**********************************************************************
        button_configs = [
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
        if button.text() == "Regresar":
            self.cambioP = MainPersonal()

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
        self.new_animation.setDuration(150)  
        self.new_animation.setStartValue(0.0)  
        self.new_animation.setEndValue(1.0)  
        self.new_animation.start()
        self.close()

#################################### Interfaz para ver lista empleado #######################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPersonal()
    window.show()
    sys.exit(app.exec())
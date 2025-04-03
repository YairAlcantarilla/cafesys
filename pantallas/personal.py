import sys
import conexion
import p_inicio, Caja, P_Registros, main_p, personal, login, p_inventario, P_Ajustes
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                           QWidget, QPushButton, QGraphicsOpacityEffect, QLineEdit,
                           QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                           QRadioButton, QButtonGroup, QGridLayout, QComboBox)
#################################### Interfaz principal de personal #######################################################

class MainPersonal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(1366, 768)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/Mpersonal.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(160, 145, 650, 555)  
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels([
            "ID", "Contraseña", "Nombre", "Teléfono", "Dirección", "ID Puesto"
        ])

        
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

        
        header = self.table_widget.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        
        self.cargar_datos()

        button_configs = [
            ["Caja", 30, 152, 60, 50],
            ["Reportes", 30, 227, 60, 50],
            ["Productos", 30, 303, 60, 50],
            ["Personal", 30, 378, 60, 50],
            ["Inventario", 30, 454, 60, 50],
            ["Ajustes", 30, 530, 60, 50],
            ["Salir", 30, 605, 60, 50],
            #################################
            ["AgregarE", 875, 144, 344, 55],
            ["EliminarE", 875, 225, 344, 55],
            ["EditarE", 875, 306, 344, 55],
            ["GenerarQR", 875, 387, 344, 55],  
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
                background-color: rgba(255, 255, 255, 30);
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
            self.agregar_window = AgregarE()
            self.agregar_window.show()
        elif button.text() == "EliminarE":
            self.eliminar_window = EliminarE()
            self.eliminar_window.show()
        elif button.text() == "EditarE":
            self.editar_window = EditarE()
            self.editar_window.show()
        elif button.text() == "GenerarQR":
            self.qr_window = GenerarQR()
            self.qr_window.show()
        elif button.text() == "RegresarE":
            self.cambioP = p_inicio.MainWindow()
            self.fade_out()
        elif button.text() == "Caja":
            respuesta = QMessageBox.question(
                self,
                "Confirmación",
                "¿Está seguro de que desea salir de personal?",
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
                "¿Está seguro de que desea salir de personal?",
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
                "¿Está seguro de que desea salir de personal?",
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
                "¿Está seguro de que desea salir de personal?",
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
                "¿Está seguro de que desea salir de personal?",
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
                "¿Está seguro de que desea salir de Personal?",
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
        self.setFixedSize(500, 650)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ADDPER.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Modificar input_configs para quitar el campo de ocupación
        input_configs = [
            ["Nombre", 195, 152, 270, 40],
            ["Direccion", 195, 225, 270, 40],
            ["Telefono", 195, 298, 270, 40], 
            ["Contraseña", 195, 371, 270, 40] 
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
        self.admin_radio.move(195, 446)  # Mover a la posición del input eliminado
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
        self.cajero_radio.move(350, 446)  # 30 píxeles debajo del radio de administrador
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
            ["Confirmar", 122, 547, 100, 60],  # Movido a la izquierda
            ["Regresar", 279, 547, 100, 60],   # Movido a la derecha
        ]
        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 70);
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
            self.close()
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
                "nombre": self.inputs[0].text(),        
                "Direccion": self.inputs[1].text(),     
                "telefono": telefono,                   
                "contrasenna": self.inputs[3].text(),   
                "ID_Puesto": tipo_usuario              
            }

            if all(datos.values()):
                try:
                    conexion.insertar_dato("usuario", datos)
                    # Update main window if it exists
                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, MainPersonal):
                            widget.cargar_datos()
                    QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", "Por favor completa todos los campos.")
#################################### Interfaz para eliminar empleado #######################################################
class EliminarE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliminar usuario")
        self.setFixedSize(400, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/ELIMU.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Agregar ComboBox para seleccionar usuario
        self.usuario_combo = QComboBox(self)
        self.usuario_combo.setGeometry(74, 200, 252, 40)
        self.usuario_combo.setStyleSheet("""
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
                image: none;
            }
        """)
        self.cargar_usuarios()

        button_configs = [
            ["Eliminar", 74, 402, 97, 61],
            ["Regresar", 229, 402, 97, 61],
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 80);
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

    def cargar_usuarios(self):
        try:
            usuarios = conexion.mostrar_usuarios()
            self.usuario_combo.addItem("Seleccionar usuario")
            for usuario in usuarios:
                self.usuario_combo.addItem(f"{usuario[0]} - {usuario[2]}")  # ID - Nombre
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar usuarios: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.close()
        elif button.text() == "Eliminar":
            if self.usuario_combo.currentText() != "Seleccionar usuario":
                try:
                    id_usuario = self.usuario_combo.currentText().split(" - ")[0]

                    usuarios = conexion.mostrar_usuarios()
                    

                    usuario_actual = None
                    for usuario in usuarios:
                        if str(usuario[0]) == id_usuario:
                            usuario_actual = usuario
                            break
                    
                    if usuario_actual is None:
                        QMessageBox.warning(self, "Error", "Usuario no encontrado")
                        return
                    

                    if usuario_actual[5] == 1:  # ID_Puesto = 1 es de administrador
                        # Checkeo de admins
                        count_admin = sum(1 for user in usuarios if user[5] == 1)
                        
                        if count_admin <= 1:
                            QMessageBox.warning(
                                self, 
                                "Advertencia", 
                                "No se puede eliminar el usuario. Debe haber al menos un administrador en el sistema."
                            )
                            return

                    reply = QMessageBox.question(
                        self, 
                        'Confirmación',
                        '¿Está seguro de eliminar este usuario?',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        conexion.eliminar_usuario(id_usuario)
                        QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                        self.cargar_usuarios()
                        for widget in QApplication.topLevelWidgets():
                            if isinstance(widget, MainPersonal):
                                widget.cargar_datos()
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
        self.setFixedSize(500, 650)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/EDITP2.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        # Dropdown para seleccionar usuario
        self.usuario_combo = QComboBox(self)
        self.usuario_combo.setGeometry(195, 152, 270, 40)
        self.usuario_combo.setStyleSheet("""
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
        """)
        self.cargar_usuarios()
        self.usuario_combo.currentIndexChanged.connect(self.usuario_seleccionado)

        # Campos de entrada
        input_configs = [
            ["Direccion", 195, 225, 270, 40],
            ["Telefono", 195, 298, 270, 40], 
            ["Contraseña", 195, 371, 270, 40] 
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
        
        # Radio buttons para tipo de usuario
        self.tipo_usuario_group = QButtonGroup(self)
        
        self.admin_radio = QRadioButton("Administrador", self)
        self.admin_radio.move(195, 446)
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
        
        self.cajero_radio = QRadioButton("Cajero", self)
        self.cajero_radio.move(350, 446)
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
        
        self.tipo_usuario_group.addButton(self.admin_radio)
        self.tipo_usuario_group.addButton(self.cajero_radio)

        button_configs = [
            ["Confirmar", 122, 547, 100, 60],
            ["Regresar", 279, 547, 100, 60],
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 70);
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

    def cargar_usuarios(self):
        try:
            usuarios = conexion.mostrar_usuarios()
            self.usuario_combo.addItem("Seleccionar usuario")
            for usuario in usuarios:
                self.usuario_combo.addItem(f"{usuario[0]} - {usuario[2]}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar usuarios: {str(e)}")

    def usuario_seleccionado(self):
        if self.usuario_combo.currentText() != "Seleccionar usuario":
            try:
                id_usuario = self.usuario_combo.currentText().split(" - ")[0]
                usuarios = conexion.mostrar_usuarios()
                
                usuario_actual = None
                for usuario in usuarios:
                    if str(usuario[0]) == id_usuario:
                        usuario_actual = usuario
                        break
                
                if usuario_actual:
                    self.inputs[0].setText(str(usuario_actual[4]))  # Dirección
                    self.inputs[1].setText(str(usuario_actual[3]))  # Teléfono
                    self.inputs[2].setText(str(usuario_actual[1]))  # Contraseña
                    
                    # Seleccionar el radio button correspondiente
                    if usuario_actual[5] == 1:  # ID_Puesto
                        self.admin_radio.setChecked(True)
                    else:
                        self.cajero_radio.setChecked(True)
                else:
                    QMessageBox.warning(self, "Error", "Usuario no encontrado")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar datos del usuario: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.close()
        elif button.text() == "Confirmar":
            if self.usuario_combo.currentText() == "Seleccionar usuario":
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un usuario")
                return

            tipo_usuario = 1 if self.admin_radio.isChecked() else 2

            # Validar teléfono
            telefono = self.inputs[1].text()
            if not telefono.isdigit() or len(telefono) > 10:
                QMessageBox.warning(self, "Advertencia", "El teléfono debe contener solo números y máximo 10 dígitos")
                return

            try:
                id_usuario = self.usuario_combo.currentText().split(" - ")[0]
                datos = {
                    "Direccion": self.inputs[0].text(),
                    "telefono": telefono,
                    "contrasenna": self.inputs[2].text(),
                    "ID_Puesto": tipo_usuario
                }

                if all(datos.values()):
                    # Verificar si es el último administrador
                    if tipo_usuario == 2:  # Si está cambiando a cajero
                        usuarios = conexion.mostrar_usuarios()
                        count_admin = sum(1 for user in usuarios if user[5] == 1)
                        usuario_actual = next((user for user in usuarios if str(user[0]) == id_usuario), None)
                        
                        if usuario_actual and usuario_actual[5] == 1 and count_admin <= 1:
                            QMessageBox.warning(
                                self, 
                                "Advertencia", 
                                "No se puede cambiar el rol. Debe haber al menos un administrador en el sistema."
                            )
                            return

                    conexion.actualizar_usuario(id_usuario, datos)
                    QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
                    # Actualizar ventana principal
                    for widget in QApplication.topLevelWidgets():
                        if isinstance(widget, MainPersonal):
                            widget.cargar_datos()
                    self.close()
                else:
                    QMessageBox.warning(self, "Advertencia", "Por favor complete todos los campos")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {str(e)}")

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

#################################### Interfaz para generar QR #######################################################
class GenerarQR(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generar QR")
        self.setFixedSize(500, 650)

        central_widget = QWidget(selgf)
        self.setCentralWidget(central_widget)
        
        background_label = QLabel(central_widget)
        pixmap = QPixmap('imagenes/GQR.png')
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(background_label)

        # Dropdown menu para usuarios
        self.usuario_combo = QComboBox(self)
        self.usuario_combo.setGeometry(195, 152, 270, 40)
        self.usuario_combo.setStyleSheet("""
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
        """)
        self.cargar_usuarios()

        # Label para mostrar el QR
        self.qr_label = QLabel(self)
        self.qr_label.setGeometry(195, 210, 270, 270)  # Position below dropdown
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("""
            QLabel {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
            }
        """)

        button_configs = [
            ["Generar QR", 122, 547, 100, 60],
            ["Regresar", 279, 547, 100, 60],
        ]

        self.buttons = []
        for name, x, y, width, height in button_configs:
            button = QPushButton(name, self)
            button.setFixedSize(width, height)
            button.move(x, y)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 70);
                    border: 0px solid white;
                    border-radius: 10px;
                    color: transparent;
                }
            """)
            button.clicked.connect(self.button_clicked)
            self.buttons.append(button)

    def cargar_usuarios(self):
        try:
            usuarios = conexion.mostrar_usuarios()
            self.usuario_combo.addItem("Seleccionar usuario")
            for usuario in usuarios:
                self.usuario_combo.addItem(f"{usuario[0]} - {usuario[2]}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar usuarios: {str(e)}")

    def button_clicked(self):
        button = self.sender()
        if button.text() == "Regresar":
            self.close()
        elif button.text() == "Generar QR":
            if self.usuario_combo.currentText() != "Seleccionar usuario":
                try:
                    id_usuario = self.usuario_combo.currentText().split(" - ")[0]
                    datos_usuario = conexion.obtener_datos_usuario(id_usuario)
                    
                    if datos_usuario:
                        qr_path = conexion.generar_qr_usuario(datos_usuario[0], datos_usuario[1])
                        if qr_path:
                            # Mostrar QR en la ventana
                            qr_pixmap = QPixmap(qr_path)
                            scaled_pixmap = qr_pixmap.scaled(
                                270, 270,
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation
                            )
                            self.qr_label.setPixmap(scaled_pixmap)
                            QMessageBox.information(self, "Éxito", 
                                f"Código QR generado correctamente")
                        else:
                            QMessageBox.warning(self, "Error", 
                                "No se pudo generar el código QR")
                    else:
                        QMessageBox.warning(self, "Error", 
                            "No se encontraron datos del usuario")
                except Exception as e:
                    QMessageBox.critical(self, "Error", 
                        f"Error al generar QR: {str(e)}")
            else:
                QMessageBox.warning(self, "Advertencia", 
                    "Por favor seleccione un usuario")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPersonal()
    window.show()
    sys.exit(app.exec())
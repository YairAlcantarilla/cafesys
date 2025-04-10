from PyQt6.QtWidgets import (
    QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt6.QtCore import pyqtSignal

class TransferList(QWidget):
    itemsChanged = pyqtSignal()

    def __init__(self, title_left="Disponibles", title_right="Seleccionados"):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Left column
        left_layout = QVBoxLayout()
        left_label = QLabel(title_left)
        left_label.setStyleSheet("color: #E6AA68;")
        self.left_list = QListWidget()
        self.left_list.setStyleSheet("""
            QListWidget {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
            }
            QListWidget::item:selected {
                background-color: #E6AA68;
                color: #111A2D;
            }
        """)
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.left_list)
        
        # Buttons
        button_layout = QVBoxLayout()
        self.to_right_btn = QPushButton(">")
        self.to_left_btn = QPushButton("<")
        button_layout.addStretch()
        button_layout.addWidget(self.to_right_btn)
        button_layout.addWidget(self.to_left_btn)
        button_layout.addStretch()
        
        # Right column
        right_layout = QVBoxLayout()
        right_label = QLabel(title_right)
        right_label.setStyleSheet("color: #E6AA68;")
        self.right_list = QListWidget()
        self.right_list.setStyleSheet("""
            QListWidget {
                background-color: #111A2D;
                border: 1px solid #E6AA68;
                border-radius: 10px;
                color: #E6AA68;
            }
            QListWidget::item:selected {
                background-color: #E6AA68;
                color: #111A2D;
            }
        """)
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.right_list)
        
        layout.addLayout(left_layout)
        layout.addLayout(button_layout)
        layout.addLayout(right_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.to_right_btn.clicked.connect(self.move_to_right)
        self.to_left_btn.clicked.connect(self.move_to_left)
        
        # Style buttons
        button_style = """
            QPushButton {
                background-color: #E6AA68;
                border-radius: 10px;
                padding: 5px;
                min-width: 30px;
                color: #111A2D;
            }
            QPushButton:hover {
                background-color: #D69958;
            }
        """
        self.to_right_btn.setStyleSheet(button_style)
        self.to_left_btn.setStyleSheet(button_style)

    def move_to_right(self):
        items = self.left_list.selectedItems()
        for item in items:
            self.left_list.takeItem(self.left_list.row(item))
            self.right_list.addItem(item.text())
        self.itemsChanged.emit()

    def move_to_left(self):
        items = self.right_list.selectedItems()
        for item in items:
            self.right_list.takeItem(self.right_list.row(item))
            self.left_list.addItem(item.text())
        self.itemsChanged.emit()

    def get_selected_items(self):
        return [self.right_list.item(i).text() for i in range(self.right_list.count())]

    def set_available_items(self, items):
        self.left_list.clear()
        self.left_list.addItems(items)

    def set_selected_items(self, items):
        self.right_list.clear()
        self.right_list.addItems(items)
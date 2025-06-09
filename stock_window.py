# stock_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from product_service import get_all_products

class StockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Produits et Stock")
        self.setGeometry(200, 200, 800, 400)
        self.init_ui()
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel("📦 Liste des Produits et Stock")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Référence", "Quantité", "Prix", "Catégorie"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_products(self):
        products = get_all_products()
        self.table.setRowCount(0)

        for row_idx, product in enumerate(products):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate([product[0], product[2], product[1], product[3], product[4], product[5]]):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

            # Highlight low stock
            if int(product[3]) < 5:
                for col in range(self.table.columnCount()):
                    self.table.item(row_idx, col).setBackground(QColor(255, 220, 220))

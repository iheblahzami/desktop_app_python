from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QGroupBox, QInputDialog
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from database import init_db
from product_service import add_product, get_all_products, delete_product, update_product, get_low_stock_products,search_products

import csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Stock")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()
        init_db()
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("🧱 Gestion de Stock - Quincaillerie")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Form
        form_group = QGroupBox("🛠 Ajouter ou Modifier un Produit")
        form_layout = QVBoxLayout()

        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Référence")
        form_layout.addWidget(self.reference_input)

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom")
        form_layout.addWidget(self.nom_input)

        self.quantite_input = QLineEdit()
        self.quantite_input.setPlaceholderText("Quantité")
        form_layout.addWidget(self.quantite_input)

        self.categorie_input = QLineEdit()
        self.categorie_input.setPlaceholderText("Catégorie")
        form_layout.addWidget(self.categorie_input)


        self.fournisseur_input = QLineEdit()
        self.fournisseur_input.setPlaceholderText("Fournisseur")
        form_layout.addWidget(self.fournisseur_input)

        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Image (chemin)")
        form_layout.addWidget(self.image_input)

        browse_button = QPushButton("Parcourir")
        browse_button.clicked.connect(self.browse_image)
        form_layout.addWidget(browse_button)

        self.add_button = QPushButton("Ajouter / Mettre à jour")
        self.add_button.clicked.connect(self.handle_add_update)
        form_layout.addWidget(self.add_button)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)


        

        # Recherche et filtre
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un produit")
        self.search_input.textChanged.connect(self.search_product)
        search_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tous", "Catégorie"])
        self.filter_combo.currentIndexChanged.connect(self.filter_products)
        search_layout.addWidget(self.filter_combo)

        layout.addLayout(search_layout)

        self.low_stock_btn = QPushButton("Afficher les produits en faible stock")
        self.low_stock_btn.clicked.connect(self.show_low_stock_products)
        layout.addWidget(self.low_stock_btn)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Quantité", "Catégorie", "Fournisseur", "Image"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Actions
        actions_layout = QHBoxLayout()
        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self.delete_selected)
        actions_layout.addWidget(delete_btn)

        edit_btn = QPushButton("Modifier")
        edit_btn.clicked.connect(self.edit_selected)
        actions_layout.addWidget(edit_btn)

        export_btn = QPushButton("Exporter CSV")
        export_btn.clicked.connect(self.export_csv)
        actions_layout.addWidget(export_btn)

        layout.addLayout(actions_layout)

        self.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 6px;
            }
            QLabel {
                font-size: 13px;
            }
            QTableWidget {
                font-size: 13px;
            }
        """)

        self.setLayout(layout)

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_input.setText(file_name)

    def handle_add_update(self):
        try:
            reference = self.reference_input.text().strip()
            nom = self.nom_input.text().strip()
            quantite_text = self.quantite_input.text().strip()
            categorie = self.categorie_input.text().strip()
            fournisseur = self.fournisseur_input.text().strip()
            image = self.image_input.text().strip()

            if not reference or not nom or not quantite_text:
                raise ValueError("Champs obligatoires manquants")

            quantite = int(quantite_text)

            product_id = getattr(self, 'editing_product_id', None)
            if product_id:
                update_product(product_id, reference, nom,  categorie, quantite, fournisseur, image)

                self.add_button.setText("Ajouter / Mettre à jour")
                del self.editing_product_id
            else:
                add_product(reference, nom,  categorie, quantite, fournisseur, image)

            self.clear_form()
            self.load_products()

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs requis et entrer une quantité valide.")

    def clear_form(self):
        self.reference_input.clear()
        self.nom_input.clear()
        self.quantite_input.clear()
        self.categorie_input.clear()
        
        self.fournisseur_input.clear()
        self.image_input.clear()

    def load_products(self, products=None):
        if products is None:
            products = get_all_products()

        self.table.setRowCount(0)

        for row_idx, product in enumerate(products):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

        # Highlight low stock rows
        for row in range(self.table.rowCount()):
            try:
                quantity_item = self.table.item(row, 2)
                if quantity_item and int(quantity_item.text()) < 5:
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item:
                            item.setBackground(QColor(255, 200, 200))
            except ValueError:
                continue

    def delete_selected(self):
        selected = self.table.currentRow()
        if selected != -1:
            product_id = int(self.table.item(selected, 0).text())
            delete_product(product_id)
            self.load_products()

    def edit_selected(self):
        selected = self.table.currentRow()
        if selected != -1:
            self.editing_product_id = int(self.table.item(selected, 0).text())
            self.reference_input.setText(self.table.item(selected, 1).text())
            self.nom_input.setText(self.table.item(selected, 1).text())
            self.quantite_input.setText(self.table.item(selected, 2).text())
            self.categorie_input.setText(self.table.item(selected, 3).text())
            self.fournisseur_input.setText(self.table.item(selected, 4).text())
            self.image_input.setText(self.table.item(selected, 5).text())
            self.add_button.setText("Mettre à jour")


    def search_product(self, text):
        if text.strip():
            filtered = search_products(text)
            self.load_products(filtered)
        else:
            self.load_products()

    def filter_products(self):
        criterion = self.filter_combo.currentText()
        products = get_all_products()

        if criterion == "Catégorie":
            values = {p[3] for p in products if p[3]}
        else:
            self.load_products()
            return

        if values:
            selected_value, ok = QInputDialog.getItem(self, f"Sélectionner un {criterion.lower()}", f"{criterion}s disponibles", list(values), 0, False)
            if ok:
                if criterion == "Catégorie":
                    filtered = [p for p in products if p[3] == selected_value]
                else:
                    filtered = [p for p in products if p[4] == selected_value]
                self.load_products(filtered)

    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter CSV", "", "CSV Files (*.csv)")
        if file_path:
            products = get_all_products()
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nom", "Quantité", "Catégorie",  "Fournisseur", "Image"])
                for p in products:
                    writer.writerow(p)

    def show_low_stock_products(self):
        low_stock = get_low_stock_products(threshold=5)
        if not low_stock:
            QMessageBox.information(self, "Stock", "Tous les produits ont un stock suffisant.")
            return

        msg = "Produits en faible stock (< 5):\n\n"
        for ref, name,  cat, qty, price, img in low_stock:
            msg += f"- {name} (Réf: {ref}) : {qty} en stock\n"

        QMessageBox.warning(self, "Stock faible", msg)

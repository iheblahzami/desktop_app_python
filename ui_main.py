from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from database import init_db
from product_service import add_product, get_all_products, delete_product, update_product
import csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Stock")
        self.setWindowIcon(QIcon("assets/icon.png"))  # Optional app icon
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()
        init_db()
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout()

        # App Header
        header_label = QLabel("🧱 Gestion de Stock - Quincaillerie")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Formulaire group
        form_group = QGroupBox("🛠 Ajouter ou Modifier un Produit")
        form_group_layout = QVBoxLayout()

        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("reference")
        form_group_layout.addWidget(self.reference_input)

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom")
        form_group_layout.addWidget(self.nom_input)

        self.quantite_input = QLineEdit()
        self.quantite_input.setPlaceholderText("Quantité")
        form_group_layout.addWidget(self.quantite_input)

        self.categorie_input = QLineEdit()
        self.categorie_input.setPlaceholderText("Catégorie")
        form_group_layout.addWidget(self.categorie_input)

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Type")
        form_group_layout.addWidget(self.type_input)

        self.fournisseur_input = QLineEdit()
        self.fournisseur_input.setPlaceholderText("Fournisseur")
        form_group_layout.addWidget(self.fournisseur_input)

        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Image (chemin)")
        form_group_layout.addWidget(self.image_input)

        browse_button = QPushButton("Parcourir")
        browse_button.clicked.connect(self.browse_image)
        form_group_layout.addWidget(browse_button)

        self.add_button = QPushButton("Ajouter / Mettre à jour")
        self.add_button.clicked.connect(self.handle_add_update)
        form_group_layout.addWidget(self.add_button)

        form_group.setLayout(form_group_layout)
        layout.addWidget(form_group)

        # Recherche et filtre
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un produit")
        self.search_input.textChanged.connect(self.search_product)
        search_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Tous")
        self.filter_combo.addItem("Catégorie")
        self.filter_combo.addItem("Type")
        self.filter_combo.currentIndexChanged.connect(self.filter_products)
        search_layout.addWidget(self.filter_combo)

        layout.addLayout(search_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Quantité", "Catégorie", "Type", "Fournisseur", "Image"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)
        layout.setStretchFactor(self.table, 1)

        # Actions
        actions_layout = QHBoxLayout()
        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self.delete_selected)
        delete_btn.setToolTip("Supprimer ce produit")
        actions_layout.addWidget(delete_btn)

        edit_btn = QPushButton("Modifier")
        edit_btn.clicked.connect(self.edit_selected)
        edit_btn.setToolTip("Modifier ce produit")
        actions_layout.addWidget(edit_btn)

        export_btn = QPushButton("Exporter CSV")
        export_btn.clicked.connect(self.export_csv)
        actions_layout.addWidget(export_btn)

        layout.addLayout(actions_layout)

        # Global stylesheet
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
        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_input.setText(file_name)

    def handle_add_update(self):
        try:
            product_id = getattr(self, 'editing_product_id', None)
            reference =self.reference_input.text()
            nom = self.nom_input.text()
            quantite = int(self.quantite_input.text())
            categorie = self.categorie_input.text()
            type = self.type_input.text()
            fournisseur = self.fournisseur_input.text()
            image = self.image_input.text()

            if product_id:
                update_product(product_id,reference, nom, quantite, categorie, type, fournisseur, image)
                self.add_button.setText("Ajouter / Mettre à jour")
                del self.editing_product_id
            else:
                add_product(reference, nom, quantite, categorie, type, fournisseur, image)

            self.clear_form()
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une quantité valide.")

    def load_products(self, products=None):
        if products is None:
            products = get_all_products()

        self.table.setRowCount(0)
        for row_data in products:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, data in enumerate(row_data):
                self.table.setItem(row_position, col, QTableWidgetItem(str(data)))

    def clear_form(self):
        self.nom_input.clear()
        self.quantite_input.clear()
        self.categorie_input.clear()
        self.type_input.clear()
        self.fournisseur_input.clear()
        self.image_input.clear()

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
            self.nom_input.setText(self.table.item(selected, 1).text())
            self.quantite_input.setText(self.table.item(selected, 2).text())
            self.categorie_input.setText(self.table.item(selected, 3).text())
            self.type_input.setText(self.table.item(selected, 4).text())
            self.fournisseur_input.setText(self.table.item(selected, 5).text())
            self.image_input.setText(self.table.item(selected, 6).text())
            self.add_button.setText("Mettre à jour")

    def search_product(self, text):
        products = get_all_products()
        filtered = [p for p in products if text.lower() in p[1].lower()]
        self.load_products(filtered)

    def filter_products(self):
        criterion = self.filter_combo.currentText()
        products = get_all_products()

        if criterion == "Catégorie":
            values = {p[3] for p in products}
        elif criterion == "Type":
            values = {p[4] for p in products}
        else:
            self.load_products()
            return

        if values:
            selected_value, ok = QFileDialog.getItem(self, f"Sélectionner un {criterion.lower()}", f"{criterion}s disponibles", list(values), 0, False)
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
                writer.writerow(["ID", "Nom", "Quantité", "Catégorie", "Type", "Fournisseur", "Image"])
                for p in products:
                    writer.writerow(p)

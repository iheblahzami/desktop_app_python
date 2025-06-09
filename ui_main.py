from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QGroupBox, QInputDialog
)
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt
from database import init_db
from product_service import add_product, get_all_products, delete_product, update_product, get_low_stock_products, search_products

from stock_window import StockWindow

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

        self.prix_input = QLineEdit()
        self.prix_input.setPlaceholderText("Prix")
        form_layout.addWidget(self.prix_input)

        self.categorie_input = QLineEdit()
        self.categorie_input.setPlaceholderText("Catégorie")
        form_layout.addWidget(self.categorie_input)

        self.fournisseur_input = QLineEdit()
        self.fournisseur_input.setPlaceholderText("Fournisseur")
        form_layout.addWidget(self.fournisseur_input)

        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText("Image (chemin)")
        form_layout.addWidget(self.image_input)

        self.image_preview = QLabel()
        self.image_preview.setFixedSize(100, 100)
        self.image_preview.setScaledContents(True)
        self.image_preview.setStyleSheet("border: 1px solid gray;")
        form_layout.addWidget(self.image_preview)

        browse_button = QPushButton("Parcourir")
        browse_button.clicked.connect(self.browse_image)
        form_layout.addWidget(browse_button)

        self.add_button = QPushButton("Ajouter / Mettre à jour")
        self.add_button.clicked.connect(self.handle_add_update)
        form_layout.addWidget(self.add_button)

        reset_btn = QPushButton("Réinitialiser")
        reset_btn.clicked.connect(self.clear_form)
        form_layout.addWidget(reset_btn)

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

        self.view_stock_btn = QPushButton("📊 Voir les Produits et le Stock")
        self.view_stock_btn.clicked.connect(self.open_stock_window)
        layout.addWidget(self.view_stock_btn)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Référence", "Nom", "Quantité", "Prix", "Catégorie", "Fournisseur", "Image"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Actions
        actions_layout = QHBoxLayout()

        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self.delete_selected)
        delete_btn.setStyleSheet("background-color: #ef9a9a; font-weight: bold;")
        actions_layout.addWidget(delete_btn)

        edit_btn = QPushButton("Modifier")
        edit_btn.clicked.connect(self.edit_selected)
        edit_btn.setStyleSheet("background-color: #ffcc80; font-weight: bold;")
        actions_layout.addWidget(edit_btn)

        export_btn = QPushButton("Exporter CSV")
        export_btn.clicked.connect(self.export_csv)
        export_btn.setStyleSheet("background-color: #a5d6a7; font-weight: bold;")
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
        
        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignRight)
        self.stats_label.setStyleSheet("font-size: 12px; color: gray; margin: 5px;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_input.setText(file_name)
            self.image_preview.setPixmap(QPixmap(file_name))

    def handle_add_update(self):
        try:
            reference = self.reference_input.text().strip()
            nom = self.nom_input.text().strip()
            quantite_text = self.quantite_input.text().strip()
            prix_text = self.prix_input.text().strip()
            categorie = self.categorie_input.text().strip()
            fournisseur = self.fournisseur_input.text().strip()
            image = self.image_input.text().strip()

            if not reference or not nom or not quantite_text or not prix_text:
                raise ValueError("Champs obligatoires manquants (référence, nom, quantité, prix)")

            quantite = int(quantite_text)
            prix = float(prix_text)

            product_id = getattr(self, 'editing_product_id', None)
            if product_id:
                update_product(product_id, reference, nom, quantite, prix, categorie, fournisseur, image)
                self.add_button.setText("Ajouter / Mettre à jour")
                del self.editing_product_id
            else:
                add_product(reference, nom, quantite, prix, categorie, fournisseur, image)
            
            QMessageBox.information(self, "Succès", "Produit ajouté/mis à jour avec succès.")
            self.clear_form()
            self.load_products()

        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e) or "Erreur de saisie.")

    def clear_form(self):
        self.reference_input.clear()
        self.nom_input.clear()
        self.quantite_input.clear()
        self.prix_input.clear()
        self.categorie_input.clear()
        self.fournisseur_input.clear()
        self.image_input.clear()
        self.image_preview.clear()
        
        # Reset button text if we were editing
        if hasattr(self, 'editing_product_id'):
            del self.editing_product_id
            self.add_button.setText("Ajouter / Mettre à jour")

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
        low_stock_count = 0
        for row in range(self.table.rowCount()):
            try:
                quantity_item = self.table.item(row, 3)  # Column 3 is quantity
                if quantity_item and int(quantity_item.text()) < 5:
                    low_stock_count += 1
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        if item:
                            item.setBackground(QColor(255, 200, 200))
            except ValueError:
                continue

        # Update stats
        total = len(products)
        self.stats_label.setText(f"Total produits : {total} | Stock faible : {low_stock_count}")

    def delete_selected(self):
        selected = self.table.currentRow()
        if selected != -1:
            product_id = int(self.table.item(selected, 0).text())
            reply = QMessageBox.question(self, "Confirmation", "Supprimer ce produit ?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                delete_product(product_id)
                QMessageBox.information(self, "Supprimé", "Produit supprimé avec succès.")
                self.load_products()

    def edit_selected(self):
        selected = self.table.currentRow()
        if selected != -1:
            product_id = int(self.table.item(selected, 0).text())
            reference = self.table.item(selected, 1).text()
            nom = self.table.item(selected, 2).text()
            quantite = self.table.item(selected, 3).text()
            prix = self.table.item(selected, 4).text()
            categorie = self.table.item(selected, 5).text()
            fournisseur = self.table.item(selected, 6).text()
            image = self.table.item(selected, 7).text()

            self.reference_input.setText(reference)
            self.nom_input.setText(nom)
            self.quantite_input.setText(quantite)
            self.prix_input.setText(prix)
            self.categorie_input.setText(categorie)
            self.fournisseur.setText(fournisseur)
            self.image_input.setText(image)

            # Set image preview
            if image and image != "None":
                try:
                    self.image_preview.setPixmap(QPixmap(image))
                except:
                    self.image_preview.clear()
            else:
                self.image_preview.clear()

            self.editing_product_id = product_id
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
            values = {p[5] for p in products if p[5]}  # Colonne 5 = Catégorie
        else:
            self.load_products()
            return

        if values:
            selected_value, ok = QInputDialog.getItem(
                self,
                f"Sélectionner une {criterion.lower()}",
                f"{criterion}s disponibles",
                sorted(list(values)),
                0,
                False
            )
            if ok:
                if criterion == "Catégorie":
                    filtered = [p for p in products if p[5] == selected_value]
                else:
                    filtered = products
                self.load_products(filtered)
            else:
                self.load_products()
        else:
            QMessageBox.information(self, "Info", f"Aucune {criterion.lower()} disponible.")



    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter CSV", "", "CSV Files (*.csv)")
        if file_path:
            products = get_all_products()
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Référence", "Nom", "Quantité", "Prix", "Catégorie", "Fournisseur", "Image"])
                for p in products:
                    writer.writerow(p)

    def show_low_stock_products(self):
        low_stock = get_low_stock_products(threshold=5)
        if not low_stock:
            QMessageBox.information(self, "Stock", "Tous les produits ont un stock suffisant.")
            return

        msg = "Produits en faible stock (< 5):\n\n"
        for prod in low_stock:
            msg += f"Réf: {prod[0]}, Nom: {prod[1]}, Quantité: {prod[3]}\n"
        QMessageBox.information(self, "Stock faible", msg)
        
        # Convert low_stock results to full product format for display
        products = get_all_products()
        low_stock_full = [p for p in products if p[3] < 5]  # Filter products with quantity < 5
        self.load_products(low_stock_full)


    def open_stock_window(self):
        self.stock_window = StockWindow()
        self.stock_window.show()
    
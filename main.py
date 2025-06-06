import sys
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow
from database import init_db

if __name__ == "__main__":
    init_db()  # Initialize database

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QPushButton,QMessageBox
from .upload_page import UploadPage
from services.database import Database

class UnlabelledOptionsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unlabelled Options")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.upload_button = QPushButton("Upload Images")
        self.upload_button.clicked.connect(self.open_upload_page)
        layout.addWidget(self.upload_button)

        self.label_button = QPushButton("Label Images")
        self.label_button.clicked.connect(self.label_images)  # Placeholder functionality
        layout.addWidget(self.label_button)

    def open_upload_page(self):
        self.hide()
        self.upload_page = UploadPage()
        self.upload_page.show()

    #def label_images(self):
    #   QMessageBox.information(self, "Label Images", "Label images functionality to be implemented.")
    def label_images(self):
        from .all_images_page import AllImagesWindow
        # Open a window to display all images from the 'all_images' database
        try:
            database = Database()
            db =  database.client['all_images']
            self.all_images_window = AllImagesWindow(db)
            self.all_images_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
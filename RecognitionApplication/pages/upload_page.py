import os
import hashlib
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTabWidget, QDialog, QScrollArea, QCheckBox, QGridLayout, QDialogButtonBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class UploadPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Upload Example")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()

        self.upload_dir = os.path.join(os.getcwd(), 'uploaded_images')
        os.makedirs(self.upload_dir, exist_ok=True)

        self.option_upload_single()
        self.option_upload_multiple()

        self.tab_widget.addTab(self.tab_1, "Tab 1")
        self.tab_widget.addTab(self.tab_2, "Tab 2")
        self.layout.addWidget(self.tab_widget)

        self.return_back = QPushButton("Return Home")
        self.return_back.clicked.connect(self.return_home)
        self.layout.addWidget(self.return_back)

        self.back = QPushButton("Back")
        self.back.clicked.connect(self.back_prevpage)
        self.layout.addWidget(self.back)

    def option_upload_single(self):
        layout = QFormLayout()
        self.upload_button_single = QPushButton("Upload Image")
        self.upload_button_single.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button_single)

        self.image_label_single = QLabel("No Image Uploaded")
        self.image_label_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label_single)

        self.tab_1.setLayout(layout)

    def option_upload_multiple(self):
        layout = QFormLayout()
        self.upload_button_multiple = QPushButton("Upload Multiple Images")
        self.upload_button_multiple.clicked.connect(self.upload_images)
        layout.addWidget(self.upload_button_multiple)

        self.tab_2.setLayout(layout)

    def upload_image(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", 
                                                       "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
            if file_name:
                if self.image_exists(file_name):
                    QMessageBox.warning(self, "Duplicate Image", "This image already exists in the directory.")
                else:
                    selected_files = self.confirm_upload([file_name])
                    if selected_files:
                        pixmap = QPixmap(selected_files[0])
                        self.image_label_single.setPixmap(pixmap.scaled(self.image_label_single.size(), Qt.AspectRatioMode.KeepAspectRatio))
                        self.image_label_single.setText("")
                        self.save_image(selected_files[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def upload_images(self):
        try:
            file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", 
                                                         "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
            if file_names:
                new_files = [file_name for file_name in file_names if not self.image_exists(file_name)]
                selected_files = self.confirm_upload(new_files)
                if selected_files:
                    for file_name in selected_files:
                        self.save_image(file_name)
                    QMessageBox.information(self, "Images Uploaded", f"Uploaded {len(selected_files)} images.")
                    if len(selected_files) < len(new_files):
                        QMessageBox.warning(self, "Duplicate Images", f"{len(new_files) - len(selected_files)} images were duplicates and were not uploaded.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def save_image(self, file_name):
        try:
            base_name = os.path.basename(file_name)
            name, ext = os.path.splitext(base_name)
            destination = os.path.join(self.upload_dir, base_name)
            count = 1

            while os.path.exists(destination):
                new_name = f"{name} ({count}){ext}"
                destination = os.path.join(self.upload_dir, new_name)
                count += 1

            with open(file_name, 'rb') as src_file:
                image_data = src_file.read()
                with open(destination, 'wb') as dest_file:
                    dest_file.write(image_data)
            print(f"Image saved to directory with path: {destination}")            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {e}")
    
    def image_exists(self, file_name):
        try:
            with open(file_name, 'rb') as image_file:
                image_data = image_file.read()
                image_hash = hashlib.sha256(image_data).hexdigest()
                for existing_file in os.listdir(self.upload_dir):
                    existing_file_path = os.path.join(self.upload_dir, existing_file)
                    with open(existing_file_path, 'rb') as existing_image_file:
                        existing_image_data = existing_image_file.read()
                        existing_image_hash = hashlib.sha256(existing_image_data).hexdigest()
                        if existing_image_hash == image_hash:
                            return True
                return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to check if image exists: {e}")
            return False    

    def return_home(self):
        self.hide()
        from .starting_page import StartingPage
        self.start = StartingPage()
        self.start.show()

    def back_prevpage(self):
        self.hide()
        from .unlabeled_options_page import UnlabelledOptionsPage
        self.start = UnlabelledOptionsPage()
        self.start.show()
    
    def confirm_upload(self, file_names):
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Upload")
        dialog.setGeometry(100, 100, 600, 400)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        checkboxes = []
        for i, file_name in enumerate(file_names):
            pixmap = QPixmap(file_name)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

            checkbox = QCheckBox()
            checkbox.setChecked(True)

            checkboxes.append((checkbox, file_name))
            scroll_layout.addWidget(image_label, i // 4, (i % 4) * 2)
            scroll_layout.addWidget(checkbox, i // 4, (i % 4) * 2 + 1)

        scroll_area.setWidget(scroll_content)

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(scroll_area)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(button_box)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            selected_files = [file_name for checkbox, file_name in checkboxes if checkbox.isChecked()]
            return selected_files
        else:
            return []

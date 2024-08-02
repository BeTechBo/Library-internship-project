from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
import os
import shutil

class AllImagesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('All Images')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        self.load_images_from_folder('uploaded_images')
        
        self.layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        self.layout.addWidget(back_button)

        show_button = QPushButton("Show")
        show_button.clicked.connect(self.show_item)
        self.layout.addWidget(show_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(delete_button)

        # Connect double-click signal to the slot
        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)

    def refresh_list(self):
        self.listWidget.clear()
        self.load_images_from_folder('uploaded_images')
        
    def load_images_from_folder(self, folder_path):
        # Load all images from a folder and display them in the list widget
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                item = QListWidgetItem()
                pixmap = QPixmap(os.path.join(folder_path, filename))
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(pixmap))
                item.setText(filename)
                self.listWidget.addItem(item)

    def show_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            print(f"Selected item text: {item_text}")
            # Optionally, show a message box with the selected item's text
            QMessageBox.information(self, "Selected Item", f"Selected item: {item_text}")

    def delete_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            reply = QMessageBox.question(self, 'Delete Confirmation',
                                         f"Are you sure you want to delete {item_text}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Delete the file from the folder
                folder_path = 'uploaded_images'
                file_path = os.path.join(folder_path, item_text)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.listWidget.takeItem(self.listWidget.row(current_item))
                    QMessageBox.information(self, "Delete", f"{item_text} has been deleted.")
                else:
                    QMessageBox.warning(self, "Delete", f"{item_text} not found.")

    def item_double_clicked(self, item):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            print(f"Double-clicked on: {item_text}")

            from .labeling_picture_page import LabellingPic
            self.label_image = LabellingPic(item_text, 'uploaded_images')
            self.label_image.show()
            self.label_image.closeEvent = lambda event: self.on_labelling_pic_close(event, item_text, self.label_image.final_move_image)
            
    def on_labelling_pic_close(self, event, item_text, final_move_image):
        if (final_move_image == True):
            self.move_image_to_labelled_folder(item_text)
        self.refresh_list()
        event.accept()
    
    def move_image_to_labelled_folder(self, item_text):
        src_path = os.path.join('uploaded_images', item_text)
        dest_path = os.path.join('labelled_images', item_text)
    
        # Create the folder if it doesn't exist
        labelled_folder = 'labelled_images'
        if not os.path.exists(labelled_folder):
            os.makedirs(labelled_folder)
    
        # Check if the same content image already exists
        same_content = False
        existing_file_path = None
        for dest_filename in os.listdir('labelled_images'):
            full_dest_path = os.path.join('labelled_images', dest_filename)
            if open(src_path, 'rb').read() == open(full_dest_path, 'rb').read():
                same_content = True
                existing_file_path = full_dest_path
                break
    
        if same_content:
            replace_reply = QMessageBox.question(self, 'Replace Confirmation',
                                                 f"This image already exists in 'labelled images'. Do you want to replace it?",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                 QMessageBox.StandardButton.No)
            if replace_reply == QMessageBox.StandardButton.Yes:
                if existing_file_path:
                    os.remove(existing_file_path)  # Remove the existing image
            else:
                return
    
        if os.path.exists(dest_path) and not same_content:
            base_name, extension = os.path.splitext(item_text)
            counter = 1
            new_dest_path = os.path.join('labelled_images', f"{base_name} ({counter}){extension}")
            while os.path.exists(new_dest_path):
                counter += 1
                new_dest_path = os.path.join('labelled_images', f"{base_name} ({counter}){extension}")
            dest_path = new_dest_path
    
        shutil.move(src_path, dest_path)
        self.listWidget.takeItem(self.listWidget.row(self.listWidget.findItems(item_text, Qt.MatchFlag.MatchExactly)[0]))
        QMessageBox.information(self, "Move", f"{item_text} has been moved to 'labelled images'.")

    def go_back(self):
        self.close()

import sys
from pages.starting_page import StartingPage
from PyQt6.QtWidgets import QApplication
from styles.style import StyleSheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet.style())
    main_window = StartingPage()
    main_window.show()
    sys.exit(app.exec())

class StyleSheet:
    @staticmethod
    def style():
        return """
            * {
                font-family: 'Impact', sans-serif;
                background-color: #1e1e1e;
            }
            QPushButton {
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton{
                background-color: #BB86FC;
            }
            QPushButton:hover {
                background-color: #D9A4FF;
            }
        """
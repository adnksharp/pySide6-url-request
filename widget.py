import sys

from PySide6.QtWidgets import QApplication, QWidget

from ui_form import Ui_Widget
from text_ui import Ui_Widget as Ui_TextWidget

class TextWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)        
        self.ui = Ui_TextWidget()
        self.ui.setupUi(self)
        
        self.parent = parent

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())

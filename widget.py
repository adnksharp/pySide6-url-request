import sys
import requests as curl
from bs4 import BeautifulSoup

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import QSize

from ui_form import Ui_Widget
from ui_text import Ui_Widget  as Ui_TextWidget

class WebContent(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)        
        self.ui = Ui_TextWidget()
        self.ui.setupUi(self)
        
        self.parent = parent
        
    def update(self, data):
        data = '\n'.join(l for l in data.splitlines() if l.strip())
        data.replace('\r', '')
        #labels = []
        self.parent.clearHeaders(self.ui.layout)
        for i in data.split('\n'):
            label = QLabel(i)
            self.parent.labelConf(QSizePolicy.Policy.Expanding, label)
            label.setWordWrap(True)
            print(label.text())
            self.ui.layout.addWidget(label)

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        self.ui.textEdit.textChanged.connect(self.loaduri)
        
        self.text = WebContent(parent=self)
        
    def labelConf(self, arg, label):
        sizePolicy = QSizePolicy(arg, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
        
        label.setSizePolicy(sizePolicy)
    
    def clearHeaders(self, layout):
        if layout is not None:
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item.widget():
                    widget = item.widget()
                    #widget.setParent(None)
                    widget.deleteLater()
                elif item.layout():
                    self.clearHeaders(item.layout())
        
    def loaduri(self):
        try:
            self.clearHeaders(self.ui.headers)
        except:
            return

        try:
            uri = curl.get(self.ui.textEdit.toPlainText())
        except:
            return
        
        for i in uri.headers:
            box = QHBoxLayout()
            labels = [QLabel(i + ': '), QLabel(uri.headers[i])]
            
            self.labelConf(QSizePolicy.Policy.Minimum, labels[0])
            labels[0].setStyleSheet('color: #f75d54')
            
            labels[1].setMaximumSize(QSize(1300, 16777215))
            self.labelConf(QSizePolicy.Policy.Expanding, labels[1])
            
            for x  in labels:
                x.setWordWrap(True)
                box.addWidget(x)
            self.ui.headers.addLayout(box)
            
        self.text.show()
        self.text.update(BeautifulSoup(uri.text).get_text('\n'))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.showMaximized()
    sys.exit(app.exec())

# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget

from UI.Ui_common import Ui_Common

class CommonInterface(QWidget, Ui_Common):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
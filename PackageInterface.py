# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget

from UI.Ui_package import Ui_Package

class PackageInterface(QWidget, Ui_Package):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
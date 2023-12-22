# coding:utf-8
import configparser

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager

from UI.Ui_setting import Ui_Form

class SettingInterface(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.HyperlinkLabel.setUrl('https://github.com/Eanya-Tonic/MihiroToolbox')
        
        self.ImageLabel.setPixmap(QPixmap('img/logo.png').scaledToHeight(100))

        # 选择主题
        
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        theme = conf.get('DEFAULT', 'theme')
        
        self.ThemeBox.addItem('跟随系统')
        self.ThemeBox.addItem('浅色')
        self.ThemeBox.addItem('深色')
        
        self.ThemeBox.setCurrentIndex(int(theme))
        self.ThemeBox.currentIndexChanged.connect(self.ThemeBoxChanged)
        
        # 关闭开屏画面
        splash = conf.get('DEFAULT', 'splash')
        self.LaunchCheck.setChecked(bool(int(splash)))
        self.LaunchCheck.clicked.connect(self.LaunchCheckClicked)
        
        # 开关ScrollArea
        ScrollUI = conf.get('DEFAULT', 'ScrollUI')
        
        self.ThemeBox_2.addItem('禁用')
        self.ThemeBox_2.addItem('启用')
        
        self.ThemeBox_2.setCurrentIndex(int(ScrollUI))
        self.ThemeBox_2.currentIndexChanged.connect(self.ScrollChanged)
        
        
    # 选择主题
    def ThemeBoxChanged(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        conf.set('DEFAULT', 'theme', str(self.ThemeBox.currentIndex()))
        conf.write(open('config.ini', 'w'))
        
        InfoBar.info(
                title='提示',
                content="主题修改重启应用后生效",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self
            )
    
    # 开关ScrollArea
    def ScrollChanged(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        conf.set('DEFAULT', 'ScrollUI', str(self.ThemeBox_2.currentIndex()))
        conf.write(open('config.ini', 'w'))
        
        InfoBar.info(
                title='提示',
                content="重启应用后生效",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self
            )
        
    # 关闭开屏画面
    def LaunchCheckClicked(self):
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        conf.set('DEFAULT', 'splash', str(int(self.LaunchCheck.isChecked())))
        conf.write(open('config.ini', 'w'))
    
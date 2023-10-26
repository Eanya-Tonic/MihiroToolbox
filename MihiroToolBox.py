# coding:utf-8
import sys
import configparser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen

from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationItemPosition, setTheme, Theme

from VideoInterface import VideoInterface
from AudioInterface import AudioInterface
from CommonInterface import CommonInterface
from PackageInterface import PackageInterface
from SettingInterface import SettingInterface


class MihiroToolBox(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('MihiroToolBox')
        self.setWindowIcon(QIcon('img/logo.png'))
        self.move(500, 75)

        # 添加视频子界面
        self.VideoInterface = VideoInterface(self)
        self.addSubInterface(self.VideoInterface, FluentIcon.VIDEO, '视频')

        # 添加音频子界面
        self.AudioInterface = AudioInterface(self)
        self.addSubInterface(self.AudioInterface, FluentIcon.MUSIC, '音频')

        # 添加通用子界面
        self.CommonInterface = CommonInterface(self)
        self.addSubInterface(self.CommonInterface,
                             FluentIcon.APPLICATION, '常用')

        # 添加封装子界面
        self.PackageInterface = PackageInterface(self)
        self.addSubInterface(self.PackageInterface, FluentIcon.MEDIA, '封装')

        # 添加设置子界面
        self.SettingInterface = SettingInterface(self)
        self.addSubInterface(
            self.SettingInterface, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)


if __name__ == '__main__':
    
    # 读取配置文件
    conf = configparser.ConfigParser()

    conf.read('config.ini')
    theme = conf.get('DEFAULT', 'theme')
    showSplash = conf.get('DEFAULT', 'splash')
    
    # 启用高分屏
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 设置主题
    if(theme == '0'):
        setTheme(Theme.AUTO)
    elif(theme == '1'):
        setTheme(Theme.LIGHT)
    elif(theme == '2'):
        setTheme(Theme.DARK)
    
    app = QApplication(sys.argv)
    

    splash = QSplashScreen()
    splash.setPixmap(QPixmap(r'img/splash.png'))
    if(showSplash == '1'):
        splash.show()
    
    ex = MihiroToolBox()
    ex.show()
    splash.finish(ex)  # 主界面加载完成后隐藏
    splash.deleteLater()
    sys.exit(app.exec_())

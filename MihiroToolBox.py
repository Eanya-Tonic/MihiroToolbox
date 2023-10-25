# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import SplitFluentWindow, FluentIcon

from VideoInterface import VideoInterface
from AudioInterface import AudioInterface
from CommonInterface import CommonInterface
from PackageInterface import PackageInterface


class MihiroToolBox(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('MihiroToolBox')

        # 添加视频子界面
        self.VideoInterface = VideoInterface(self)
        self.addSubInterface(self.VideoInterface, FluentIcon.VIDEO, '视频')

        # 添加音频子界面
        self.AudioInterface = AudioInterface(self)
        self.addSubInterface(self.AudioInterface, FluentIcon.MUSIC, '音频')

        # 添加通用子界面
        self.CommonInterface = CommonInterface(self)
        self.addSubInterface(self.CommonInterface, FluentIcon.LABEL, '常用')
        
        # 添加封装子界面
        self.PackageInterface = PackageInterface(self)
        self.addSubInterface(self.PackageInterface, FluentIcon.MEDIA, '封装')


if __name__ == '__main__':
    # 启用高分屏
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    ex = MihiroToolBox()
    ex.show()
    sys.exit(app.exec_())

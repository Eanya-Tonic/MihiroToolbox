# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget,QFileDialog,QApplication
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from functools import partial
import os
from threading import Thread

from UI.Ui_package import Ui_Package

class PackageInterface(QWidget, Ui_Package):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # 隐藏ProgressBar
        self.ProgressBar1.setVisible(0)
        self.ProgressBar2.setVisible(0)
        self.ProgressBar3.setVisible(0)
        
        # 文件选择
        self.InputButton.clicked.connect(partial(self.FileSelect, self.InputLine))
        self.OutputButton.clicked.connect(partial(self.FileSelect, self.OutputLine))
        self.AudioButton.clicked.connect(partial(self.FileSelect, self.AudioLine))
        self.InputButton_2.clicked.connect(partial(self.FileSelect, self.InputLine_2))
        self.AudioButton_2.clicked.connect(partial(self.FileSelect, self.AudioLine_2))
        self.OutputButton_2.clicked.connect(partial(self.FileSelect, self.OutputLine_2))
        self.TextButton.clicked.connect(partial(self.FileSelect, self.TextLine))
        self.OutputButton_3.clicked.connect(partial(self.FileSelect, self.OutputLine_3))
        
        # 文件自动填充
        self.InputLine.textChanged.connect(partial(self.AutoFill, self.InputLine, self.OutputLine, 1))
        self.InputLine_2.textChanged.connect(partial(self.AutoFill, self.InputLine_2, self.OutputLine_2, 2))
        
        # 粘贴地址
        self.PasteButton.clicked.connect(partial(self.Paste, self.AddressLine))
        
        # 操作开始按钮
        self.MP4Start.clicked.connect(self.MP4Func)
        self.MP4Start.setWindowIconText("")
        self.MP4Start.windowIconTextChanged.connect(
            self.MP4Complte)
        
        self.MkvStart.clicked.connect(self.MkvFunc)
        self.MkvStart.setWindowIconText("")
        self.MkvStart.windowIconTextChanged.connect(
            self.MkvComplte)

        self.DownloadButton.clicked.connect(self.DownloadFunc)
        self.DownloadButton.setWindowIconText("")
        self.DownloadButton.windowIconTextChanged.connect(
            self.DownloadComplte)
        
        
    # 文件选择函数
    def FileSelect(self, TargetLine):
        dir = QFileDialog()
        dir.setDirectory(os.getcwd())
        if dir.exec_():      # 判断是否选择了文件
            FilePath = dir.selectedFiles()
            TargetLine.setText(FilePath[0])
        
    # 自动填充函数
    def AutoFill(self, SourceLine, TargetLine, Type):
        FilePath = SourceLine.text()
        if FilePath == "":
            return
        FileExt = os.path.splitext(FilePath)[1]
        FilePath = os.path.splitext(FilePath)[0]
        if(Type == 1):
            NewFilePath = FilePath + '_output.mp4'
        elif(Type == 2):
            NewFilePath = FilePath + '_output.mkv'
        TargetLine.setText(NewFilePath)

    # 粘贴函数
    def Paste(self, TargetLine):
        TargetLine.setText(QApplication.clipboard().text())
        
    # MP4封装函数
    def MP4Func(self):
        # 地址缺失
        if(self.InputLine.text() == '' or self.OutputLine.text() == ''):
            InfoBar.error(
                title='未定义地址',
                content="请确认你是否已经设定了正确的输入输出地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            return

        ProcseeCmd = "tools\\ffmpeg -hide_banner -i \"" + self.InputLine.text() + "\" "
        # 封装音频
        if(self.AudioLine.text() != ''):
            ProcseeCmd += "-i \"" + self.AudioLine.text() + "\" "
        ProcseeCmd += "-c:v copy -c:a copy -strict experimental -y \"" + self.OutputLine.text() + "\""
        
        thread_01 = Thread(target=self.MP4Thread, args=(ProcseeCmd,))
        thread_01.start()
    
    # MP4封装线程
    def MP4Thread(self, ProcseeCmd):
        self.MP4Start.setWindowIconText(" ")
        self.ProgressBar1.setVisible(1)
        self.MP4Start.setEnabled(0)
        
        os.system(ProcseeCmd)
        
        self.MP4Start.setWindowIconText("")
        self.ProgressBar1.setVisible(0)
        self.MP4Start.setEnabled(1)
    
    # MP4封装完成
    def MP4Complte(self):
        if(self.MP4Start.windowIconText() == ""):
            InfoBar.success(
                title='封装完成',
                content="请确认是否封装成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            
    # MKV封装函数
    def MkvFunc(self):
        # 地址缺失
        if(self.InputLine_2.text() == '' or self.OutputLine_2.text() == ''):
            InfoBar.error(
                title='未定义地址',
                content="请确认你是否已经设定了正确的输入输出地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            return

        ProcseeCmd = "tools\\ffmpeg -hide_banner -i \"" + self.InputLine_2.text() + "\" "
        # 封装音频
        if(self.AudioLine_2.text() != ''):
            ProcseeCmd += "-i \"" + self.AudioLine_2.text() + "\" "
        # 封装字幕
        if(self.TextLine.text() != ''):
            ProcseeCmd += "-i \"" + self.TextLine.text() + "\" "
        ProcseeCmd += "-c:v copy -c:a copy -strict experimental -y \"" + self.OutputLine_2.text() + "\""
        
        thread_02 = Thread(target=self.MkvThread, args=(ProcseeCmd,))
        thread_02.start()
        
    # MKV封装线程
    def MkvThread(self, ProcseeCmd):
        self.MkvStart.setWindowIconText(" ")
        self.ProgressBar2.setVisible(1)
        self.MkvStart.setEnabled(0)
        
        os.system(ProcseeCmd)
        
        self.MkvStart.setWindowIconText("")
        self.ProgressBar2.setVisible(0)
        self.MkvStart.setEnabled(1)
    
    # MKV封装完成
    def MkvComplte(self):
        if(self.MkvStart.windowIconText() == ""):
            InfoBar.success(
                title='封装完成',
                content="请确认是否封装成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
    
    # 下载函数
    def DownloadFunc(self):
        # 地址缺失
        if(self.AddressLine.text() == '' or self.OutputLine_3.text() == ''):
            InfoBar.error(
                title='未定义地址',
                content="请确认你是否已经设定了正确的下载或输出地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            return
        
        ProcseeCmd = "tools\\ffmpeg -i \"" + self.AddressLine.text() + "\" -y \"" + self.OutputLine_3.text() + "\""
        
        thread_03 = Thread(target=self.DownloadThread, args=(ProcseeCmd,))
        thread_03.start()
        
    # 下载线程
    def DownloadThread(self, ProcseeCmd):
        self.DownloadButton.setWindowIconText(" ")
        self.ProgressBar3.setVisible(1)
        self.DownloadButton.setEnabled(0)
        
        os.system(ProcseeCmd)
        
        self.DownloadButton.setWindowIconText("")
        self.ProgressBar3.setVisible(0)
        self.DownloadButton.setEnabled(1)
    
    # 下载完成
    def DownloadComplte(self):
        if(self.DownloadButton.windowIconText() == ""):
            InfoBar.success(
                title='下载完成',
                content="请确认是否下载成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
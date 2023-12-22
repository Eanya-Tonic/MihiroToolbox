# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget,QFileDialog
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from functools import partial
import os
from threading import Thread

from UI.Ui_common import Ui_Common


class CommonInterface(QWidget, Ui_Common):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 音频参数
        self.BitrateNum.setValue(128)
        self.FpsNum.setValue(24)
        self.CrfNum.setValue(24)

        # 硬件加速
        self.HardAccler.addItem("软件")
        self.HardAccler.addItem("Nvidia")
        self.HardAccler.addItem("AMD")
        self.HardAccler.addItem("Intel")

        # 隐藏ProgressBar
        self.ProgressBar1.setVisible(0)
        self.ProgressBar2.setVisible(0)
        self.ProgressBar3.setVisible(0)

        # 截取视频
        self.StartTimeLine.setText('00:00:00')
        self.EndTimeLine.setText('00:00:20')

        # 旋转视频
        self.OptionChoice.addItem('顺时针90度')
        self.OptionChoice.addItem('逆时针90度')
        self.OptionChoice.addItem('180度')
        self.OptionChoice.addItem('水平翻转')
        self.OptionChoice.addItem('垂直翻转')

        # 操作开始按钮
        self.ProcessStartButton.clicked.connect(self.ProcessFunc)
        self.ProcessStartButton.setWindowIconText("")
        self.ProcessStartButton.windowIconTextChanged.connect(
            self.ProcessComplte)

        self.ClipVideoButton.clicked.connect(self.ClipFunc)
        self.ClipVideoButton.setWindowIconText("")
        self.ClipVideoButton.windowIconTextChanged.connect(self.ClipComplte)

        self.TransposeButton.clicked.connect(self.TransposeFunc)
        self.TransposeButton.setWindowIconText("")
        self.TransposeButton.windowIconTextChanged.connect(
            self.TransposeComplte)

        # 文件选择
        self.InputButton.clicked.connect(
            partial(self.FileSelect, self.InputLine))
        self.AudioInputButton.clicked.connect(
            partial(self.FileSelect, self.AudioInputLine))
        self.VideoOutputButton_2.clicked.connect(
            partial(self.FileSelect, self.VideoOutputLine_2))

        self.VideoInputButton.clicked.connect(
            partial(self.FileSelect, self.VideoInputLine))
        self.VideoOutputButton.clicked.connect(
            partial(self.FileSelect, self.VideoOutputLine))
        
        # 文件自动填充
        self.VideoInputLine.textChanged.connect(
            partial(self.AutoFill, self.VideoInputLine, self.VideoOutputLine, 2))
        self.AudioInputLine.textChanged.connect(
            partial(self.AutoFill, self.AudioInputLine, self.VideoOutputLine_2, 1))

    # 文件选择函数
    '''
    输入: 选择文件的目标LineEdit
    输出: 无输出
    '''
    def FileSelect(self, TargetLine):
        dir = QFileDialog()
        dir.setDirectory(os.getcwd())
        if dir.exec_():      # 判断是否选择了文件
            FilePath = dir.selectedFiles()
            TargetLine.setText(FilePath[0])
    
    # 自动填充函数
    '''
    输入: 选择文件的源LineEdit, 自动同步的目标LineEdit, 自动填充后缀名类型 1是mp4 2是保留原本的后缀名
    输出: 无输出
    '''
    def AutoFill(self, SourceLine, TargetLine, Type):
        FilePath = SourceLine.text()
        if FilePath == "":
            return
        FileExt = os.path.splitext(FilePath)[1]
        FilePath = os.path.splitext(FilePath)[0]
        if(Type == 1):
            NewFilePath = FilePath + '_output.mp4'
        elif(Type == 2):
            NewFilePath = FilePath + '_output' + FileExt
        TargetLine.setText(NewFilePath)

    # 一图流控制
    def ProcessFunc(self):
        # 地址缺失
        if(self.InputLine.text() == '' or self.VideoOutputLine_2.text() == '' or self.AudioInputLine.text() == ''):
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

        ProcessCmd = "tools\\ffmpeg -hide_banner -loop 1 " 
        
        # 硬件加速
        if(self.HardAccler.currentIndex() == 0):
            pass
        elif(self.HardAccler.currentIndex() == 1):
            ProcessCmd += "-hwaccel nvdec "
        elif(self.HardAccler.currentIndex() == 2):
            ProcessCmd += "-hwaccel amf "
        elif(self.HardAccler.currentIndex() == 3):
            ProcessCmd += "-hwaccel qsv "
        
        ProcessCmd += "-i \"" + self.InputLine.text() + "\" " + "-i \"" + self.AudioInputLine.text() + "\" -y -shortest "

        # 音频参数
        ProcessCmd += "-c:a aac -b:a " + str(self.BitrateNum.value()) + "k "

        # 视频参数
        ProcessCmd += "-r " + str(self.FpsNum.value()) + \
            " -crf " + str(self.CrfNum.value()) + " "

        thread_01 = Thread(target=self.CmdThread01,
                           args=(ProcessCmd,))
        thread_01.start()
        
    # 多线程编码函数01
    '''
    输入: 处理指令
    输出: 无输出
    '''
    def CmdThread01(self, ProcessCmd):

        self.ProgressBar1.setVisible(1)
        self.ProcessStartButton.setText("正在压制...")
        self.ProcessStartButton.setWindowIconText(" ")
        self.ProcessStartButton.setDisabled(1)

        ProcessCmd += " \"" + self.VideoOutputLine_2.text() + "\""
        os.system(ProcessCmd)

        self.ProgressBar1.setVisible(0)
        self.ProcessStartButton.setText("开始压制")
        self.ProcessStartButton.setDisabled(0)
        self.ProcessStartButton.setWindowIconText("")
        
    # 压制完成提示
    def ProcessComplte(self):
        if(self.ProcessStartButton.text() == "开始压制"):
            InfoBar.success(
                title='任务执行完成',
                content="请确认是否压制成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            
    # 视频截取控制
    def ClipFunc(self):
        # 地址缺失
        if(self.VideoInputLine.text() == '' or self.VideoOutputLine.text() == ''):
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
        
        ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -ss " + self.StartTimeLine.text() + " -to " + self.EndTimeLine.text() + " -c copy \"" + self.VideoOutputLine.text() + "\""
        
        thread_02 = Thread(target=self.CmdThread02,
                           args=(ProcessCmd,))
        thread_02.start()
        
    # 多线程编码函数02
    '''
    输入: 处理指令
    输出: 无输出
    '''
    def CmdThread02(self,ProcessCmd):
        self.ProgressBar2.setVisible(1)
        self.ClipVideoButton.setText("正在截取...")
        self.ClipVideoButton.setWindowIconText(" ")
        self.ClipVideoButton.setDisabled(1)
        self.TransposeButton.setDisabled(1)
            
        os.system(ProcessCmd)
            
        self.ProgressBar2.setVisible(0)
        self.ClipVideoButton.setText("开始截取")
        self.ClipVideoButton.setDisabled(0)
        self.TransposeButton.setDisabled(0)
        self.ClipVideoButton.setWindowIconText("")
    
    # 截取完成提示
    def ClipComplte(self):
        if(self.ClipVideoButton.text() == "开始截取"):
            InfoBar.success(
                title='任务执行完成',
                content="请确认是否截取成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
    
    # 视频旋转控制
    def TransposeFunc(self):
        # 地址缺失
        if(self.VideoInputLine.text() == '' or self.VideoOutputLine.text() == ''):
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
        
        # 旋转参数
        if(self.OptionChoice.currentIndex() == 0):
            ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -vf \"transpose=1\" \"" + self.VideoOutputLine.text() + "\""
        elif(self.OptionChoice.currentIndex() == 1):
            ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -vf \"transpose=2\" \"" + self.VideoOutputLine.text() + "\""
        elif(self.OptionChoice.currentIndex() == 2):
            ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -vf \"transpose=2,transpose=2\" \"" + self.VideoOutputLine.text() + "\""
        elif(self.OptionChoice.currentIndex() == 3):
            ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -vf \"hflip\" \"" + self.VideoOutputLine.text() + "\""
        elif(self.OptionChoice.currentIndex() == 4):
            ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.VideoInputLine.text() + "\" -y -vf \"vflip\" \"" + self.VideoOutputLine.text() + "\""
        
        thread_03 = Thread(target=self.CmdThread03,
                           args=(ProcessCmd, ))
        thread_03.start()
        
    # 多线程编码函数03
    '''
    输入: 处理指令
    输出: 无输出
    '''
    def CmdThread03(self, ProcessCmd):
        self.ProgressBar3.setVisible(1)
        self.TransposeButton.setText("正在旋转...")
        self.TransposeButton.setWindowIconText(" ")
        self.TransposeButton.setDisabled(1)
        self.ClipVideoButton.setDisabled(1)
            
        os.system(ProcessCmd)
            
        self.ProgressBar3.setVisible(0)
        self.TransposeButton.setText("开始旋转")
        self.TransposeButton.setDisabled(0)
        self.ClipVideoButton.setDisabled(0)
        self.TransposeButton.setWindowIconText("")
        
    # 旋转完成提示
    def TransposeComplte(self):
        if(self.TransposeButton.text() == "开始旋转"):
            InfoBar.success(
                title='任务执行完成',
                content="请确认是否旋转成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
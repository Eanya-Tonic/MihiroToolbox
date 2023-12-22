# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from functools import partial
import os
from threading import Thread

# 读取配置文件
import configparser
conf = configparser.ConfigParser()

conf.read('config.ini')
Scroll = conf.get('DEFAULT', 'ScrollUI')

if(Scroll == "0"):
    from UI.Ui_audio import Ui_Audio
elif(Scroll == "1"):
    from UI_test.Ui_audio import Ui_Audio


class AudioInterface(QWidget, Ui_Audio):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 音频编码选项
        self.EncoderChioce.addItem('ACC')
        self.EncoderChioce.addItem('TTA')
        self.EncoderChioce.addItem('WAV')
        self.EncoderChioce.addItem('ALAC')
        self.EncoderChioce.addItem('FLAC')
        self.EncoderChioce.addItem('AC3')
        self.EncoderChioce.addItem('MP3')
        self.EncoderChioce.currentTextChanged.connect(self.EncoderChange)
        
        # 码率
        self.BitrateNum.setValue(128)

        # 文件选项
        self.InputButton.clicked.connect(
            partial(self.FileSelect, self.InputLine))
        self.Outputbutton.clicked.connect(
            partial(self.FileSelect, self.OutputLine))
        
        # 自动填充
        self.InputLine.textChanged.connect(
            partial(self.AutoFill, self.InputLine, self.OutputLine))
        
        # 压制选项
        self.ProcessButton.clicked.connect(self.ProcessFunc)
        self.ProcessButton.setWindowIconText("")
        self.ProcessButton.windowIconTextChanged.connect(self.ProcessComplte)
        self.ProgressBar.setVisible(0)
        

    # 文件选择函数
    '''
    输入: 选择文件的目标LineEdit
    输出: 无输出
    描述: 选择文件函数, 与界面上的浏览按钮绑定, 用于把资源管理器读取的地址传回输入框
    '''
    def FileSelect(self, TargetLine):
        dir = QFileDialog()
        dir.setDirectory(os.getcwd())
        if dir.exec_():      # 判断是否选择了文件
            FilePath = dir.selectedFiles()
            TargetLine.setText(FilePath[0])
        
    # 自动填充函数
    '''
    输入: 选择文件的源LineEdit, 自动同步的目标LineEdit
    输出: 无输出
    描述: 根据输入框内容自动填充输出框
    '''
    def AutoFill(self, SourceLine, TargetLine):
        FilePath = SourceLine.text()
        if FilePath == "":
            return
        FileExt = os.path.splitext(FilePath)[1]
        FilePath = os.path.splitext(FilePath)[0]
        NewFilePath = FilePath + '_output'

        # 根据编码器选择后缀
        if(self.EncoderChioce.text() == 'ACC'):
            NewFilePath = NewFilePath + '.m4a'
        elif(self.EncoderChioce.text() == 'TTA'):
            NewFilePath = NewFilePath + '.tta'
        elif(self.EncoderChioce.text() == 'WAV'):
            NewFilePath = NewFilePath + '.wav'
        elif(self.EncoderChioce.text() == 'ALAC'):
            NewFilePath = NewFilePath + '.m4a'
        elif(self.EncoderChioce.text() == 'FLAC'):
            NewFilePath = NewFilePath + '.flac'
        elif(self.EncoderChioce.text() == 'AC3'):
            NewFilePath = NewFilePath + '.ac3'
        elif(self.EncoderChioce.text() == 'MP3'):
            NewFilePath = NewFilePath + '.mp3'

        TargetLine.setText(NewFilePath)
                
    # 去除文件后缀名用于处理
    '''
    输入: 带有后缀名的文件地址string
    输出: 无后缀名的文件地址string
    '''
    def RemoveExt(self, FilePath):
        FilePath = os.path.splitext(FilePath)[0]
        return FilePath
                
    # 编码器选择函数
    def EncoderChange(self):
        if(self.EncoderChioce.text() == 'ACC'):
            self.BitrateNum.setDisabled(0)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.m4a')
        elif(self.EncoderChioce.text() == 'TTA'):
            self.BitrateNum.setDisabled(1)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.tta')
        elif(self.EncoderChioce.text() == 'WAV'):
            self.BitrateNum.setDisabled(1)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.wav')
        elif(self.EncoderChioce.text() == 'ALAC'):
            self.BitrateNum.setDisabled(1)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.m4a')
        elif(self.EncoderChioce.text() == 'FLAC'):
            self.BitrateNum.setDisabled(1)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.flac')
        elif(self.EncoderChioce.text() == 'AC3'):
            self.BitrateNum.setDisabled(1)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.ac3')
        elif(self.EncoderChioce.text() == 'MP3'):
            self.BitrateNum.setDisabled(0)
            if(self.OutputLine.text()!=""):
                self.OutputLine.setText(self.RemoveExt(self.OutputLine.text()) + '.mp3')

    # 压制函数
    def ProcessFunc(self):
        # 地址缺失
        if(self.InputLine.text() == '' or self.OutputLine.text() == ''):
            InfoBar.error(
                title='未定义音频地址',
                content="请确认你是否已经设定了正确的输入输出音频地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            return
        
        ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.InputLine.text() + \
            "\" -y -vn "
        
        # 设置编码器
        if(self.EncoderChioce.text() == 'ACC'):
            ProcessCmd += "-c:a aac -b:a " + str(self.BitrateNum.value()) + "k "
        elif(self.EncoderChioce.text() == 'TTA'):
            ProcessCmd += "-c:a tta "
        elif(self.EncoderChioce.text() == 'WAV'):
            ProcessCmd += "-c:a pcm_s16le "
        elif(self.EncoderChioce.text() == 'ALAC'):
            ProcessCmd += "-c:a alac "
        elif(self.EncoderChioce.text() == 'FLAC'):
            ProcessCmd += "-c:a flac "
        elif(self.EncoderChioce.text() == 'AC3'):
            ProcessCmd += "-c:a ac3 "
        elif(self.EncoderChioce.text() == 'MP3'):
            ProcessCmd += "-c:a libmp3lame -b:a " + str(self.BitrateNum.value()) + "k "
        
        print(ProcessCmd)
        
        thread_01 = Thread(target=self.CmdThread,
                           args=(ProcessCmd,))
        thread_01.start()
        
    # 多线程编码函数
    '''
    输入: 处理指令
    输出: 无输出
    '''
    def CmdThread(self, ProcessCmd):

        self.ProgressBar.setVisible(1)
        self.ProcessButton.setText("正在压制...")
        self.ProcessButton.setWindowIconText(" ")
        self.ProcessButton.setDisabled(1)

        ProcessCmd += " \"" + self.OutputLine.text() + "\""
        os.system(ProcessCmd)

        self.ProgressBar.setVisible(0)
        self.ProcessButton.setText("压制")
        self.ProcessButton.setDisabled(0)
        self.ProcessButton.setWindowIconText("")
        
    # 压制完成提示
    def ProcessComplte(self):
        if(self.ProcessButton.text() == "压制"):
            InfoBar.success(
                title='任务执行完成',
                content="请确认是否压制成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )

# coding:utf-8

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QFileDialog
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from functools import partial
import os
from threading import Thread


from UI.Ui_video import Ui_Video


class VideoInterface(QWidget, Ui_Video):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 编码选项
        self.EncoderType.addItem('x264')
        self.EncoderType.addItem('x265')

        self.DepthChoice.addItem('压制音频')
        self.DepthChoice.addItem('无音频')

        # 编码参数
        self.KbpsLabel.setVisible(0)
        self.ParmsNum.setValue(24)
        self.ButtonCRF.clicked.connect(partial(self.EncodeParms, 0))
        self.ButtonVBR.clicked.connect(partial(self.EncodeParms, 1))
        self.Button2pass.clicked.connect(partial(self.EncodeParms, 1))

        # 文件选项
        self.InputButton.clicked.connect(
            partial(self.FileSelect, self.InputLine))
        self.Outputbutton.clicked.connect(
            partial(self.FileSelect, self.OutputLine))
        self.Outputbutton_2.clicked.connect(
            partial(self.FileSelect, self.TextLine))
        
        # 文件自动填充
        self.InputLine.textChanged.connect(
             partial(self.AutoFill, self.InputLine, self.OutputLine))
        

        # 分辨率选项
        self.WidthNum.setDisabled(1)
        self.HeightNum.setDisabled(1)
        self.IfEnableSwitch.checkedChanged.connect(self.ResolutionChange)

        # 开始压制
        self.StartButton.clicked.connect(self.ProcessFunc)
        self.StartButton.setWindowIconText("")
        self.StartButton.windowIconTextChanged.connect(self.ProcessComplte)
        self.ProgressBar.setVisible(0)

        # 硬件加速
        self.HardAccler.addItem("软件")
        self.HardAccler.addItem("Nvidia")
        self.HardAccler.addItem("AMD")
        self.HardAccler.addItem("Intel")
        # CRF不支持硬件编码
        self.HardAccler.setDisabled(1)

    # 文件选择函数
    def FileSelect(self, TargetLine):
        dir = QFileDialog()
        dir.setDirectory(os.getcwd())
        if dir.exec_():      # 判断是否选择了文件
            FilePath = dir.selectedFiles()
            TargetLine.setText(FilePath[0])
    
    # 自动填充函数
    def AutoFill(self, SourceLine, TargetLine):
        FilePath = SourceLine.text()
        if FilePath == "":
            return
        FileExt = os.path.splitext(FilePath)[1]
        FilePath = os.path.splitext(FilePath)[0]
        NewFilePath = FilePath + '_output.mp4'
        TargetLine.setText(NewFilePath)

    # 自定义分辨率控制
    def ResolutionChange(self):
        if (self.IfEnableSwitch.checked):
            self.WidthNum.setDisabled(0)
            self.HeightNum.setDisabled(0)
        else:
            self.WidthNum.setDisabled(1)
            self.HeightNum.setDisabled(1)

    # 编码参数控制
    def EncodeParms(self, choice):
        # 0是CRF模式
        if(choice == 0):
            self.KbpsLabel.setVisible(0)
            self.ParmsSetTitle.setText("CRF")
            # CRF默认24，小数两位
            self.ParmsNum.setValue(24)
            self.ParmsNum.setDecimals(2)
            # CRF不支持硬件编码
            self.HardAccler.setCurrentIndex(0)
            self.HardAccler.setDisabled(1)
        # 1是VBR模式
        elif(choice == 1):
            self.KbpsLabel.setVisible(1)
            self.ParmsSetTitle.setText("目标比特率")
            # VBR默认5000，没有小数
            self.ParmsNum.setValue(5000)
            self.ParmsNum.setDecimals(0)
            # VBR支持硬件编码
            self.HardAccler.setDisabled(0)

    # 压制控制
    def ProcessFunc(self):
        # 地址缺失
        if(self.InputLine.text() == '' or self.OutputLine.text() == ''):
            InfoBar.error(
                title='未定义视频地址',
                content="请确认你是否已经设定了正确的输入输出视频地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )
            return

        ProcessCmd = "tools\\ffmpeg -hide_banner -i \"" + self.InputLine.text() + \
            "\" -y "
        ProcessCmd0 = ""
        
        # 设置音频
        if(self.DepthChoice.text() == "压制音频"):
            ProcessCmd += ""
        else:
            ProcessCmd += "-an "

        # 硬件加速编码器
        if(self.EncoderType.text() == 'x264'):
            if(self.HardAccler.text() == "软解"):
                ProcessCmd += "-vcodec libx264 "
            elif(self.HardAccler.text() == "Nvidia"):
                ProcessCmd += "-vcodec h264_nvenc "
            elif(self.HardAccler.text() == "AMD"):
                ProcessCmd += "-vcodec h264_amf "
            elif(self.HardAccler.text() == "Intel"):
                ProcessCmd += "-vcodec h264_qsv "
        else:
            if(self.HardAccler.text() == "软解"):
                ProcessCmd += "-vcodec libx265 "
            elif(self.HardAccler.text() == "Nvidia"):
                ProcessCmd += "-vcodec hevc_nvenc "
            elif(self.HardAccler.text() == "AMD"):
                ProcessCmd += "-vcodec hevc_amf "
            elif(self.HardAccler.text() == "Intel"):
                ProcessCmd += "-vcodec hevc_qsv "

        # 自定义分辨率
        if(self.IfEnableSwitch.checked):
            ProcessCmd += "-s " + \
                str(self.WidthNum.value()) + "x" + \
                str(self.HeightNum.value()) + " "

        # 按帧数截取视频
        if(self.TotalFrameNum.value() != 0):
            ProcessCmd += "-vf \"select=between(n\\," + str(
                self.StartFrameNum.value()) + "\\,"+str(self.TotalFrameNum.value())+")\" "

        # 切换CRF和VBR参数
        if(self.ButtonCRF.isChecked()):
            ProcessCmd += "-crf " + str(self.ParmsNum.value()) + " "
        elif(self.ButtonVBR.isChecked()):
            ProcessCmd += "-b:v " + str(self.ParmsNum.value()) + "K "
        else:
            ProcessCmd0 = ProcessCmd
            ProcessCmd0 += "-b:v " + \
                str(self.ParmsNum.value()) + "K -pass 1 -an -f rawvideo -y NUL"

            ProcessCmd += "-b:v " + str(self.ParmsNum.value()) + "K -pass 2 "

        thread_01 = Thread(target=self.CmdThread,
                           args=(ProcessCmd0, ProcessCmd))
        thread_01.start()

    # 多线程编码函数
    def CmdThread(self, ProcessCmd0, ProcessCmd):

        self.ProgressBar.setVisible(1)
        self.StartButton.setText("正在压制...")
        self.StartButton.setWindowIconText(" ")
        self.StartButton.setDisabled(1)

        if(self.TextLine.text() != ''):
            ProcessCmd += "-vf \"subtitles=\'" + \
                self.TextLine.text().replace(":", "\:") + "\'\""
                
            # 按帧数截取视频
            if(self.TotalFrameNum.value != 0):
                ProcessCmd += ",\"select=between(n\\," + str(
                    self.StartFrameNum.value()) + "\\,"+str(self.TotalFrameNum.value())+")\" "

        ProcessCmd += " \"" + self.OutputLine.text() + "\""
        
        if(ProcessCmd0 != ""):
            os.system(ProcessCmd0)
        os.system(ProcessCmd)

        self.ProgressBar.setVisible(0)
        self.StartButton.setText("开始压制")
        self.StartButton.setDisabled(0)
        self.StartButton.setWindowIconText("")
        
        if(self.AutoPowerOffButton.isChecked()):
            os.system('shutdown -s -t 2')

    # 压制完成提示
    def ProcessComplte(self):
        if(self.StartButton.text() == "开始压制"):
            InfoBar.success(
                title='任务执行完成',
                content="请确认是否压制成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=6000,
                parent=self
            )

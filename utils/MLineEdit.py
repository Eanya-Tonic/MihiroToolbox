#coding:utf-8

from qfluentwidgets import LineEdit

# 重载LineEdit类实现文件拖放
class MLineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        # 拖拽多文件只取第一个地址
        filePath = filePathList.split('\n')[0]
        # 去除文件地址前缀的特定字符
        filePath = filePath.replace('file:///', '', 1)
        self.setText(filePath)
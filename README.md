<p align="center"> <img src="https://github.com/Eanya-Tonic/MihiroToolbox/blob/main/img/logo_big.png" style="width:200px;" /> </p>  <h1 align="center">真寻工具箱</h1>  <p align="center">一个基于PyQt-FluentUI开发的FFmpeg图形化界面程序 </p>

![image](https://github.com/Eanya-Tonic/MihiroToolbox/assets/74545593/d8480491-52da-4355-a5eb-bc0103d1eb31#pic_center)

真寻工具箱是一款用Python编写的音视频处理软件。基于FluentUI设计，为FFmpeg提供一个简洁易用的GUI，方便用户处理音视频。

## 下载安装
从Github Release下载：https://github.com/Eanya-Tonic/MihiroToolbox/releases
<br>
从百度网盘下载：https://pan.baidu.com/s/15DME9GT99bBgeSaEew-2dA?pwd=wbdt 提取码：wbdt

## 演示视频
**B站：**
[真寻工具箱—一个美观的FFmpeg音视频编码GUI程序](https://www.bilibili.com/video/BV1dg4y1d7F1/)

## 目前实现功能
**视频、音频、常用和封装**，并提供一个程序设置界面。在视频界面支持**H264和H265编码**，可以自定义分辨率和码率（通过**CRF、VBR或者2Pass**），在使用VBR模式时，支持打开硬件编码加速。音频支持通过**ACC、TAA、WAV、ALAC、FLAC、AC3、MP3编码器**重新编码转换，在使用ACC和MP3时，可以自定义码率。在常用标签页，提供了**一图流**（图片+音乐生成视频）和**无损截取视频**以及**旋转视频**（需重新编码）这几个常用功能。在封装页面提供了**MP4和MKV的封装**功能，并加入了一个**M3U8下载器**，方便快速从网页上获取流媒体视频。

## 更新日志
**v1.1.2 更新日志**(2024.09.18)
<br>
1.压制视频时，现在可以选择”复制音频“选项
<br>
**特别鸣谢： [#2](https://github.com/Eanya-Tonic/MihiroToolbox/issues/2) [#4](https://github.com/Eanya-Tonic/MihiroToolbox/issues/4)**
<br>
2.压制视频并选择音频模式为”压制音频“时，可以自定义音频码率
<br>
**特别鸣谢： [#2](https://github.com/Eanya-Tonic/MihiroToolbox/issues/2)**
<br>
_v1.1.2是一个小版本更新，不包含新功能，仅对之前的功能进行完善。_
<br>
<br>
**v1.1 更新日志**(2023.12.23)
<br>
1.增加拖拽文件导入的功能，现在文件可以被直接拖到选择框里了，不一定强制使用浏览导入。
<br>
**特别鸣谢**：**N495336@BiliBili** 提出的建议
<br>
2.在设置-实验性功能添加了”启用ScrollArea“的选项，在缩放不合适或界面过大的情况下启用可以增强软件的界面兼容性；目前已知问题是美观性不太好，故默认为禁用，可以按需启用。
<br>
**特别鸣谢**：**之一Yo@BiliBili** 提出的建议，不过个人实现的效果目前还不太好，接下来的版本还会再调整效果
<br>

## 后续功能展望
**v1.1 展望**
<br>
实现批量转换功能；继续优化程序UI界面；MediaInfo功能应该会尽快加入；发布一个专用的升级工具方便更新新版本；编译适用于Linux的真寻工具箱。
<br>
_推迟：_ 抽取、AVS功能预计将稍晚再做适配。
<br>
<br>
**v1.0 展望**
<br>
实现批量转换功能，加入抽取、AVS、MediaInfo等功能；加强程序稳定性。

## 参考

![未标题-spalsh](https://github.com/Eanya-Tonic/MihiroToolbox/assets/74545593/a9281e10-dc24-42d7-9547-37d2095a6240#pic_center)

灵感来源于媒体领域转码神器——小丸工具箱；在使用中由于小丸工具箱的编码并没有加入硬件加速解码的选项，仅使用软解的效率并不高；所以自己编写了一个带有硬件加速选项的媒体工具箱，提供软解、Nvidia、AMD、Intel四种选项可供按需，节约在转码时花费的时间。
> **Note**
> 硬件加速编码使用FFmpeg内置的编码器，根据不同电脑设备的支持程度和视频具体情况不同，不保证对于所有设备都能正常启用

## 引用&参考
[zhiyiYo / PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
<br>
本程序使用PyQt-Fluent-Widgets开发，感谢zhiyiYo制作的FluentUI工具包。
<br>
[FFmpeg / FFmpeg](https://github.com/FFmpeg/FFmpeg)
<br>
本程序是FFmpeg的GUI界面，音视频编解码操作均通过FFmpeg实现。
<br>
**真寻**
<br>
绪山真寻是《别当欧尼酱了！》的主角，也是本程序的名字和Icon的出处

## 特别鸣谢
[小丸工具箱](https://maruko.appinn.me/)

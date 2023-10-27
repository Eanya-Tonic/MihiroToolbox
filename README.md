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

## 后续功能展望
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

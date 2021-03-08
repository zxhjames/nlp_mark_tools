# 标注工具说明

## 目录说明
data/example.json是源文本的输入
data/records/result_01.txt是标注好的结果

## 启动过程
点击dist/mainwin.EXE即可

## 编译过程
```shell
# 确保windows上安装python3.7+ 环境

# 安装wx图形库
pip install -U wxPython

# 查看pythonw位置,用该EXE文件启动主程序
pythow.exe mainwin.py
```

## 打包过程
```shell
# 安装pyinstaller
pip install pyinstaller
pyinstaller -F mainwin.py
# exe文件将被打包到dist目录下，启动时记得在dist同级目录下拷贝一份data文件夹
```# nlp_mark_tools
# nlp_mark_tools

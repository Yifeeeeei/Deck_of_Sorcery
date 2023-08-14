# 如何使用

## 1 安装依赖

pip install -r requirements.txt

## 2 如果有需要修改 mass_producer_params_xlsx.json

对于每一类别的每一张excel表格，在**xlsx_paths**列表内放入excel表格的路径，然后将原图文件夹路径放在**drawing_paths**对应的位置，可以放入多张excel

以下部分有需要再改

设置output_path为输出路径，相应的卡牌会输出到[output_path]/[类别]/[元素]目录下

overwrite若为false，则如果output路径已经存在，会停止工作，如果overwite为true则会覆盖同名文件

general_path是存储通用素材的目录，默认素材存放在resources/general

fonts_path是存储字体文件的目录，默认字体存放在resources/fonts



## 3 运行

python -u run_mass_producer.py

运行中如果出现错误会提示在命令行中

## 4 目录结构

原画目录应该有这样的结构：[目录名]/[属性]/[卡牌名称] 不用关心后缀名，自动接受jpg,jpeg,png。

**!!!不要jiff!!!**
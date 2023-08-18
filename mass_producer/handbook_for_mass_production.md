# 如何使用大批量生成

## 1 安装依赖（如果没有安装过）

pip install -r requirements.txt

## 2 如果有需要修改 mass_producer_params_xlsx.json

对于每一类别的每一张excel表格，在**xlsx_paths**列表内放入excel表格的路径，然后将原图文件夹路径放在**drawing_paths**对应的位置，可以放入多张excel

“尺寸”为整数，1代表590*860，2代表长宽都变成2倍，以此类推

“打印版”设置为true 或者 false，true将会输出cmyk颜色图片用于打印，false输出rgb颜色图片用于电子版

以下部分有需要再改

设置output_path为输出路径，相应的卡牌会输出到[output_path]/[类别]/[元素]目录下

overwrite若为false，则如果output路径已经存在，会停止工作，如果overwite为true则会覆盖同名文件

general_path是存储通用素材的目录，默认素材存放在resources/general

fonts_path是存储字体文件的目录，默认字体存放在resources/fonts

## 3 运行

cd mass_procuder

python -u run_mass_producer.py

运行中如果出现错误会提示在命令行中

## 4 目录结构

原画目录应该有这样的结构：[目录名]/[属性]/[卡牌名称] 不用关心后缀名，自动接受jpg,jpeg,png, .jfif也可以，但是图片名称必须和对应的卡牌编号相同

# 如何使用单卡生成

## 1 安装依赖（如果没有安装过）

pip install -r requirements.txt

## 2 如果有需要修改 single_card_maker_params.json

前几项都是卡牌本身属性

"尺寸"为整数，1代表590*860，2代表长宽都变成2倍，以此类推

"原图文件夹"代表搜索原图的地方

"输出文件夹"代表输出文件的敌方
    
"打印版"设置为true 或者 false，true将会输出cmyk颜色图片用于打印，false输出rgb颜色图片用于电子版

## 3 运行

cd mass_procuder

python -u single_card_maker.py

运行中如果出现错误会提示在命令行中

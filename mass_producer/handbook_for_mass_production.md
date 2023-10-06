# 如何使用

## 1 安装依赖

```bash
pip install -r requirements.txt
```



## 2 如果有需要修改 mass_producer_params_xlsx.json

对于每一类别的每一张excel表格，在**xlsx_paths**列表内放入excel表格的路径，然后将原图文件夹路径放在**drawing_paths**对应的位置，可以放入多张excel

以下部分有需要再改

设置output_path为输出路径，相应的卡牌会输出到[output_path]/[类别]/[元素]目录下

overwrite若为false，则如果output路径已经存在，会停止工作，如果overwite为true则会覆盖同名文件

general_path是存储通用素材的目录，默认素材存放在resources/general

fonts_path是存储字体文件的目录，默认字体存放在resources/fonts



## 3 运行

```bash
python -u run_mass_producer.py
```

运行中如果出现错误会提示在命令行中

## 4 目录结构

原画目录应该有这样的结构：[目录名]/[属性]/[卡牌名称] 不用关心后缀名，自动接受jpg,jpeg,png。

**!!!不要jiff!!!**

## 5 导入TTS

现在获得的图片文件是单张卡牌，并不方便导入TTS，使用run_pack_maker.py来让讲各个文件夹中的内容整合成单张大图方便导入。

run_pack_maker.py的配置文件为pack_maker_params.json。

一些参数解释：

| 参数名               | 意义                               |
| -------------------- | ---------------------------------- |
| make_all_cards       | 是否开使用制作大图功能             |
| row_num              | 一张大图包含几行                   |
| col_num              | 一张大图包含几列                   |
| all_cards_dir        | 存放单图的目录                     |
| mixedup_elements     | 单图目录是否混放元素（默认为混放） |
| all_cards_output_dir | 输出目录                           |
|                      |                                    |

配置完成后运行

```bash
python -u run_pack_maker.py
```

得到大图

## 6 设计卡组并导出

run_pack_maker.py同样负责将编写好的卡组文件导出为大图形式

首先，需要编写特定的卡组文件

```python
# 卡组文件事例
# 卡组文件以行为单位编写
# 以井号开头的行为注释，解析时会被略过
# 每一行写一个卡牌编号，代表将一张该编号的卡加入卡组

# 空行将被直接略过

# 英雄
441001
# 使用//来进行手动换图，接下来的卡牌将开一张新的图来放
//
# 生物
141007
141008
142001
142001
142002
142002
142003
142003
142004
142004
//
# 技能
341008
341009
341010
341011
341012
//
#衍生物
140001
```

在解析卡组时，程序会判断卡组合法性，并进行相关的统计和报错

配置pack_maker_params.json中的相关参数

| 参数名                 | 意义                 |
| ---------------------- | -------------------- |
| make_single_deck       | 是否开启制作卡组功能 |
| text_txt_path          | 卡组文件路径         |
| single_deck_output_dir | 卡组输出目录         |

然后运行命令

```bash
python -u run_pack_maker.py
```

得到卡组大图

## 7 版本控制

现在已经加入自动化版本控制

在git pull之后，新的空白json文件会覆盖原本已经配置好的json文件，现在这一问题通过JsonVersionController类解决（./json_version_control.py）。在所有json文件中，添加了两项参数

```json
"use_former_version": true,
"@use_former_version": "在git pull之后，本文件会被覆盖，如果需要重拾旧版文件，请将此项设置为true"
```

如果use_former_version为true，代码将会自动取回上次运行时的json文件并覆盖新的文件，并将新的文件进行保存，所有json文件保存在back_up文件夹中，back_up文件夹不会上传到github仓库中

如果需要手动找回上一版本json，运行

```bash
python recover_former_jsons.py
```


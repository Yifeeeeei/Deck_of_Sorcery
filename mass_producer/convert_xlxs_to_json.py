# transform all excel cards into json

import os
import json
import pandas as pd
from tqdm import tqdm

from card_info import Elements, CardInfo
from mass_producer_xlsx import MassProducerXlsx


sheet_paths = [
    "sheets/2.2技能.xlsx",
    "sheets/2.2生物.xlsx",
    "sheets/2.2道具.xlsx",
    "sheets/2.2英雄.xlsx",
]
types = [
    "技能",
    "生物",
    "道具",
    "英雄",
]

xlxs_producer = MassProducerXlsx(None)

all_card_infos = []

for i in range(len(sheet_paths)):
    sheet_path = sheet_paths[i]
    current_sheets = pd.read_excel(
        sheet_path,
        sheet_name=None,
        header=0,
    )
    current_type = types[i]
    for sheet_name, df in current_sheets.items():
        for index, row in tqdm(df.iterrows()):
            try:
                card_info = xlxs_producer.get_card_info_from_row(row)
                if card_info is not None:
                    card_info.type = current_type
                    all_card_infos.append(card_info)
            except Exception as e:
                print("Error encountered when parsing row: ", row, e)
                continue
print(len(all_card_infos))


def convert_elements_to_dict(elements):
    return elements.elements_dict


def convert_card_info_to_dict(card_info):
    dict = {}
    dict["number"] = card_info.number
    dict["type"] = card_info.type  # 生物、技能、道具三选一
    dict["name"] = card_info.name
    dict["category"] = card_info.category  # 火水地光暗?

    dict["tag"] = card_info.tag  # 说明，传奇异兽、道具、咒术、法术之类的名词
    dict["description"] = card_info.description  # 描述
    dict["quote"] = card_info.quote  # 一段帅气的文字引用
    dict["elements_cost"] = convert_elements_to_dict(card_info.elements_cost)  # 左上角元素消耗
    dict["elements_gain"] = convert_elements_to_dict(card_info.elements_gain)  # 右下角元素负载
    dict["attack"] = card_info.attack  # 底部攻击力

    # 以下是生物卡的独有属性

    dict["life"] = card_info.life  # 生命值
    dict["version"] = card_info.version  # 版本号

    # 以下是技能卡的独有属性
    dict["duration"] = card_info.duration  # 冷却回合数
    dict["power"] = card_info.power  # 威力
    dict["elements_expense"] = convert_elements_to_dict(
        card_info.elements_expense
    )  # 代价（为彩笔？）
    return dict


all_card_infos_dicts = []
for card_info in all_card_infos:
    all_card_infos_dicts.append(convert_card_info_to_dict(card_info))

# save them into json
with open("all_card_infos.json", "w", encoding="utf-8") as f:
    json.dump(all_card_infos_dicts, f, ensure_ascii=False, indent=4)

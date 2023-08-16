from config import *
from card_maker import CardMaker, Elements, CardInfo
import json
import os


class SingleCardMaker:
    def keyword_element_extraction(self, sentence):
        if "光" in sentence:
            return "光"
        if "水" in sentence:
            return "水"
        if "火" in sentence:
            return "火"
        if "暗" in sentence:
            return "暗"
        if "气" in sentence:
            return "气"
        if "地" in sentence:
            return "地"
        if "无" in sentence or "?" in sentence or "？" in sentence:
            return "?"

    def dir_ele_translator(self, sentence):
        if "光" in sentence:
            return "光"
        if "水" in sentence:
            return "水"
        if "火" in sentence:
            return "火"
        if "暗" in sentence:
            return "暗"
        if "气" in sentence:
            return "气"
        if "地" in sentence:
            return "地"
        if "无" in sentence or "?" or "？" in sentence:
            return "无"

    def element_analysis(self, sentence):
        last_index = -1
        eles = Elements({})
        for i, chi in enumerate(sentence):
            if chi in self.blur_elements:
                num = int(sentence[last_index + 1 : i])
                last_index = sentence.index(chi)
                eles[self.blur_to_accurate(chi)] = num
        return eles

    def get_card_info_from_row(self, df_row):
        card_info = CardInfo()
        if "编号" in df_row.keys():
            card_info.number = str(int(df_row["编号"]))
        if "属性" in df_row.keys():
            card_info.category = self.blur_to_accurate(str(df_row["属性"]).strip())

        if "名称" in df_row.keys():
            card_info.name = str(df_row["名称"])
        if "标签" in df_row.keys():
            card_info.tag = str(df_row["标签"])
        if "生命" in df_row.keys():
            card_info.life = df_row["生命"]
        if "条件" in df_row.keys():
            card_info.elements_cost = self.element_analysis(df_row["条件"])
        if "种类" in df_row.keys():
            card_info.tag = str(df_row["种类"])
        if "负载" in df_row.keys():
            card_info.elements_gain = self.element_analysis(df_row["负载"])
        if "效果" in df_row.keys():
            card_info.description = str(df_row["效果"])
        if "引言" in df_row.keys():
            card_info.quote = str(df_row["引言"])
        if "威力" in df_row.keys():
            card_info.power = int(df_row["威力"])
        if "时间" in df_row.keys():
            card_info.duration = int(df_row["时间"])
        if "代价" in df_row.keys():
            card_info.elements_expense = self.element_analysis(df_row["代价"])
        if "版本" in df_row.keys():
            card_info.version = str(df_row["版本"])
        if card_info.number == "" or card_info.name == "" or card_info.category == "":
            # 空行
            return None

        return card_info

    def make_single_card(self, param_dict):
        card_maker = CardMaker(Config_default())
        card_info = self.get_card_info_from_row(param_dict)
        card_maker.config.drawing_path = param_dict["原图文件夹"]
        if card_info is None:
            print("invalid info")
            return
        card = card_maker.make_card(card_info)
        card.save(os.path.join(param_dict["输出文件夹"]))


param_dict = dict(json.load(open("single_card_maker_params.json", "r")))

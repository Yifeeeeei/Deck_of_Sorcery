import pandas as pd
from tqdm import tqdm
import json
import os

from config import *
from card_maker import CardMaker, CardInfo, Elements
from json_version_control import JsonVersionController


class MassProducerXlsx:
    def __init__(self, mass_producer_params_path: str):
        if mass_producer_params_path is None:
            print("No mass_producer_params_path specified, be careful!")
            self.all_elements = ["水", "火", "光", "暗", "气", "地", "?"]
            self.blur_elements = ["水", "火", "光", "暗", "气", "地", "?", "无", "？"]
            self.error_log = []
            return
        json_verson_controller = JsonVersionController(mass_producer_params_path)

        self.mass_producer_params = dict(json_verson_controller.get_json())
        config = None
        if self.mass_producer_params["排版"] == "游戏王":
            config = Config_YuGiOh(self.mass_producer_params["尺寸"])
        if self.mass_producer_params["排版"] == "万智牌":
            config = Config_Magic(self.mass_producer_params["尺寸"])

        self.card_maker_config = config
        self.card_maker_config.general_path = self.mass_producer_params["general_path"]
        self.card_maker_config.font_path = self.mass_producer_params["font_path"]
        self.all_elements = ["水", "火", "光", "暗", "气", "地", "?"]
        self.blur_elements = ["水", "火", "光", "暗", "气", "地", "?", "无", "？"]
        self.error_log = []
        self.all_card_infos = []

    def make_dir(
        self,
        dir_path: str,
    ):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def blur_to_accurate(self, ele):
        if ele == "无":
            return "?"
        if ele == "？":
            return "?"
        return ele

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
            card_info.number = "" if pd.isnull(df_row["编号"]) else str(int(df_row["编号"]))
        if "属性" in df_row.keys():
            card_info.category = (
                ""
                if pd.isnull(df_row["属性"])
                else self.blur_to_accurate(str(df_row["属性"]).strip())
            )
        if "类别" in df_row.keys():
            card_info.type = str(df_row["类别"]).strip()
        if "名称" in df_row.keys():
            card_info.name = "" if pd.isnull(df_row["名称"]) else str(df_row["名称"])
        if "标签" in df_row.keys():
            card_info.tag = "" if pd.isnull(df_row["标签"]) else str(df_row["标签"])
        if "生命" in df_row.keys():
            card_info.life = int(-1 if pd.isnull(df_row["生命"]) else df_row["生命"])
        if "条件" in df_row.keys():
            card_info.elements_cost = (
                Elements({})
                if pd.isnull(df_row["条件"])
                else self.element_analysis(df_row["条件"])
            )
        if "种类" in df_row.keys():
            card_info.tag = str(df_row["种类"])
        if "负载" in df_row.keys():
            card_info.elements_gain = (
                Elements({})
                if pd.isnull(df_row["负载"])
                else self.element_analysis(df_row["负载"])
            )
        if "效果" in df_row.keys():
            card_info.description = "" if pd.isnull(df_row["效果"]) else str(df_row["效果"])
        if "引言" in df_row.keys():
            card_info.quote = "" if pd.isnull(df_row["引言"]) else str(df_row["引言"])
        if "威力" in df_row.keys():
            card_info.power = int(-1 if pd.isnull(df_row["威力"]) else df_row["威力"])
        if "时间" in df_row.keys():
            card_info.duration = int(-1 if pd.isnull(df_row["时间"]) else df_row["时间"])
        if "代价" in df_row.keys():
            card_info.elements_expense = (
                Elements({})
                if pd.isnull(df_row["代价"])
                else self.element_analysis(df_row["代价"])
            )
        if "攻击" in df_row.keys():
            card_info.attack = int(-1 if pd.isnull(df_row["攻击"]) else df_row["攻击"])
        if "版本" in df_row.keys():
            card_info.version = "" if pd.isnull(df_row["版本"]) else str(df_row["版本"])
        if card_info.number == "" or card_info.name == "" or card_info.category == "":
            # 空行
            return None

        return card_info

    def draw_cards(self, card_type):
        if card_type not in ["生物", "技能", "道具", "英雄"]:
            raise ValueError("卡牌类型错误")
        assert len(self.mass_producer_params[card_type]["xlsx_paths"]) == len(
            self.mass_producer_params[card_type]["drawing_paths"]
        ), "xlsx_paths和drawing_paths长度不一致"

        for i in range(len(self.mass_producer_params[card_type]["xlsx_paths"])):
            current_sheets = pd.read_excel(
                self.mass_producer_params[card_type]["xlsx_paths"][i],
                sheet_name=None,
                header=0,
            )
            current_drawing_path = self.mass_producer_params[card_type][
                "drawing_paths"
            ][i]
            card_maker = CardMaker(self.card_maker_config)

            for ele in self.all_elements:
                self.make_dir(
                    os.path.join(
                        self.mass_producer_params["output_path"],
                        card_type,
                        self.dir_ele_translator(ele),
                    )
                )

            for sheet_name, df in current_sheets.items():
                print(
                    "making cards in",
                    self.mass_producer_params[card_type]["xlsx_paths"][i],
                    sheet_name,
                )

                for index, row in tqdm(df.iterrows()):
                    try:
                        card_info = self.get_card_info_from_row(row)
                    except Exception as e:
                        print("Error encountered when parsing row: ", row, e)
                        self.error_log.append(str(row) + " " + str(e))
                        continue
                    if card_info is None:
                        continue
                    if self.mass_producer_params["mixedup_elements"] is False:
                        card_maker.config.drawing_path = os.path.join(
                            current_drawing_path,
                            self.dir_ele_translator(card_info.category),
                        )
                    else:
                        card_maker.config.drawing_path = current_drawing_path
                    # add it to all_card_infos
                    card_info.type = card_type
                    self.all_card_infos.append(card_info)

                    try:
                        card_image = None
                        if self.mass_producer_params["打印版"] == False:
                            card_image = card_maker.make_card(card_info).convert("RGB")
                        else:
                            card_image = card_maker.make_card(card_info).convert("CMYK")
                        card_image.save(
                            os.path.join(
                                self.mass_producer_params["output_path"],
                                card_type,
                                self.dir_ele_translator(card_info.category),
                                str(card_info.number) + "_" + card_info.name + ".jpg",
                            )
                        )

                    except Exception as e:
                        print(
                            "Error encountered when drawing card: ", card_info.name, e
                        )
                        self.error_log.append(str(card_info) + " " + str(e))

    def convert_elements_to_dict(self, elements):
        return elements.elements_dict

    def convert_card_info_to_dict(self, card_info):
        dict = {}
        dict["number"] = card_info.number
        dict["type"] = card_info.type  # 生物、技能、道具三选一
        dict["name"] = card_info.name
        dict["category"] = card_info.category  # 火水地光暗?

        dict["tag"] = card_info.tag  # 说明，传奇异兽、道具、咒术、法术之类的名词
        dict["description"] = card_info.description  # 描述
        dict["quote"] = card_info.quote  # 一段帅气的文字引用
        dict["elements_cost"] = self.convert_elements_to_dict(
            card_info.elements_cost
        )  # 左上角元素消耗
        dict["elements_gain"] = self.convert_elements_to_dict(
            card_info.elements_gain
        )  # 右下角元素负载
        dict["attack"] = card_info.attack  # 底部攻击力

        dict["life"] = card_info.life  # 生命值
        dict["version"] = card_info.version  # 版本号

        # 以下是技能卡的独有属性
        dict["duration"] = card_info.duration  # 冷却回合数
        dict["power"] = card_info.power  # 威力
        dict["elements_expense"] = self.convert_elements_to_dict(
            card_info.elements_expense
        )  # 代价（为彩笔？）
        return dict

    def produce(self):
        # 检查输出路径
        if (
            os.path.exists(self.mass_producer_params["output_path"])
            and self.mass_producer_params["overwrite"] is False
        ):
            raise FileExistsError("输出路径已存在")
        self.card_maker = CardMaker(self.card_maker_config)

        if "生物" in self.mass_producer_params.keys():
            # 开始绘制生物牌
            if self.mass_producer_params["生物"]["skip"] is False:
                self.draw_cards("生物")
        if "技能" in self.mass_producer_params.keys():
            # 开始绘制技能牌
            if self.mass_producer_params["技能"]["skip"] is False:
                self.draw_cards("技能")
        if "道具" in self.mass_producer_params.keys():
            # 开始绘制道具牌
            if self.mass_producer_params["道具"]["skip"] is False:
                self.draw_cards("道具")
        if "英雄" in self.mass_producer_params.keys():
            # 开始绘制英雄牌
            if self.mass_producer_params["英雄"]["skip"] is False:
                self.draw_cards("英雄")
        with open(
            os.path.join(self.mass_producer_params["output_path"], "error_log.txt"), "w"
        ) as f:
            f.write("\n".join(self.error_log))
        # save all_card_infos into json
        all_card_infos_dicts = []
        for card_info in self.all_card_infos:
            all_card_infos_dicts.append(self.convert_card_info_to_dict(card_info))

        # save them into json
        with open("all_card_infos.json", "w", encoding="utf-8") as f:
            json.dump(all_card_infos_dicts, f, ensure_ascii=False, indent=4)

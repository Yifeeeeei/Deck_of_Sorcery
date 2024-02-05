from json_version_control import JsonVersionController
import json

mass_producer_dict = {
    "生物": {
        "skip": False,
        "xlsx_paths": ["sheets/2.2生物.xlsx"],
        "drawing_paths": ["牌面图片/生物"],
    },
    "技能": {
        "skip": False,
        "xlsx_paths": ["sheets/2.2技能.xlsx"],
        "drawing_paths": ["牌面图片/技能"],
    },
    "道具": {
        "skip": False,
        "xlsx_paths": ["sheets/2.2道具.xlsx"],
        "drawing_paths": ["牌面图片/道具"],
    },
    "英雄": {
        "skip": False,
        "xlsx_paths": ["sheets/2.2英雄.xlsx"],
        "drawing_paths": ["牌面图片/英雄"],
    },
    "尺寸": 2,
    "打印版": False,
    "@排版": "游戏王or万智牌",
    "排版": "游戏王",
    "overwrite": True,
    "mixedup_elements": True,
    "output_path": "output",
    "general_path": "resources/general",
    "font_path": "resources/fonts",
    "use_former_version": False,
    "@use_former_version": "在git pull之后，本文件会被覆盖，如果需要重拾旧版文件，请将此项设置为True",
}


pack_maker_dict = {
    "row_num": 5,
    "@row_num": "一共几行",
    "col_num": 6,
    "@col_num": "一共几列",
    "all_cards_dir": "./output",
    "@all_cards_dir": "卡牌的文件夹，dir/类别/属性/卡牌",
    "overwrite": True,
    "make_all_cards": True,
    "@make_all_cards": "是否生成所有卡牌，在生成所有牌以后快速将所有的牌生成到一张图片上，导入tts",
    "mixedup_elements": False,
    "@mixedup_elements": "是否将所有的元素混合在一起，只保留类别文件夹，如果为False，则会按照元素分别生成卡牌",
    "all_cards_output_dir": "./all_cards_output",
    "make_single_deck": True,
    "@make_single_deck": "是否生成单个卡组,如果True，则会按照提供的文件生成单个卡组",
    "deck_txt_paths": ["./卡组/earth.txt"],
    "@deck_txt_path": "卡组文件的路径，每一行是一张卡牌的路径，如果是相对路径，则是相对于cards_dir的路径，txt每一行为一个卡牌号",
    "single_deck_output_dir": "./deck",
    "use_former_version": False,
    "@use_former_version": "在git pull之后，本文件会被覆盖，如果需要自动重新加载旧版文件，请将此项设置为True，否则设置为False",
}

single_card_maker_dict = {
    "编号": "100001",
    "名称": "大法师 伦德萨尔",
    "类别": "生物",
    "属性": "光",
    "标签": "巫师",
    "引言": "“真是没完没了，幸好我还剩下一招，一个真正的绝活！”",
    "条件": "6光",
    "效果": "入场，遗言：使你的一个法术获得+4威力，+1重伤",
    "负载": "2光",
    "生命": 2,
    "持续时间": 0,
    "威力": 0,
    "代价": "",
    "尺寸": 2,
    "原图文件夹": ".",
    "输出文件夹": ".",
    "打印版": False,
    "@排版": "游戏王or万智牌",
    "排版": "游戏王",
}

if __name__ == "__main__":
    json_path = "mass_producer_params_xlsx.json"
    json.dump(
        mass_producer_dict,
        open(json_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    json_path = "pack_maker_params.json"
    json.dump(
        pack_maker_dict,
        open(json_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    json_path = "single_card_maker_params.json"
    json.dump(
        single_card_maker_dict,
        open(json_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )

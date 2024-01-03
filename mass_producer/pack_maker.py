import PIL.Image
import json
import os
from tqdm import tqdm
from json_version_control import JsonVersionController


class PackMaker:
    def __init__(self, pack_maker_params_path: str):
        json_verson_controller = JsonVersionController(pack_maker_params_path)
        self.pack_maker_params = dict(json_verson_controller.get_json())
        self.all_card_path_dict = {}

        for type_dir in os.listdir(self.pack_maker_params["all_cards_dir"]):
            # check if it is a dir
            if not os.path.isdir(
                os.path.join(self.pack_maker_params["all_cards_dir"], type_dir)
            ):
                continue
            for ele_dir in os.listdir(
                os.path.join(self.pack_maker_params["all_cards_dir"], type_dir)
            ):
                if not os.path.isdir(
                    os.path.join(
                        self.pack_maker_params["all_cards_dir"], type_dir, ele_dir
                    )
                ):
                    continue
                for card_file in os.listdir(
                    os.path.join(
                        self.pack_maker_params["all_cards_dir"], type_dir, ele_dir
                    )
                ):
                    if (
                        card_file.endswith(".jpg")
                        or card_file.endswith(".png")
                        or card_file.endswith(".jpeg")
                    ):
                        card_number = card_file.split("_")[0]
                        self.all_card_path_dict[card_number] = os.path.join(
                            self.pack_maker_params["all_cards_dir"],
                            type_dir,
                            ele_dir,
                            card_file,
                        )
        # check size
        self.card_size = PIL.Image.open(list(self.all_card_path_dict.values())[0]).size
        for card_path in self.all_card_path_dict.values():
            assert (
                PIL.Image.open(card_path).size == self.card_size
            ), "card size not match"
        print("card size: ", "self.card_size")
        print("all card number: ", len(self.all_card_path_dict))
        self.name_extension = (
            "_"
            + str(self.pack_maker_params["row_num"])
            + "rows"
            + str(self.pack_maker_params["col_num"])
            + "cols"
        )

    def make_all_cards_from_dir(self, source_dir: str, target_dir: str):
        if not os.path.exists(
            os.path.join(self.pack_maker_params["all_cards_output_dir"], target_dir)
        ):
            os.makedirs(
                os.path.join(self.pack_maker_params["all_cards_output_dir"], target_dir)
            )
        canvas = PIL.Image.new(
            "RGB",
            (
                self.pack_maker_params["col_num"] * self.card_size[0],
                self.pack_maker_params["row_num"] * self.card_size[1],
            ),
            (255, 255, 255),
        )
        pin_x = 0
        pin_y = 0
        counter = 0
        counter_max = (
            self.pack_maker_params["col_num"] * self.pack_maker_params["row_num"]
        )
        big_pic_counter = 0
        for ele_dir in os.listdir(source_dir):
            if not os.path.isdir(os.path.join(source_dir, ele_dir)):
                continue
            print("processing: ", source_dir, ele_dir)
            output_dir = (
                os.path.join(self.pack_maker_params["all_cards_output_dir"], target_dir)
                if self.pack_maker_params["mixedup_elements"]
                else os.path.join(
                    self.pack_maker_params["all_cards_output_dir"], target_dir, ele_dir
                )
            )
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            for card_file in tqdm(os.listdir(os.path.join(source_dir, ele_dir))):
                if (
                    card_file.endswith(".jpg")
                    or card_file.endswith(".png")
                    or card_file.endswith(".jpeg")
                ):
                    target_image = PIL.Image.open(
                        os.path.join(source_dir, ele_dir, card_file)
                    ).convert("RGB")
                    canvas.paste(
                        target_image,
                        (
                            pin_x * self.card_size[0],
                            pin_y * self.card_size[1],
                        ),
                    )
                    pin_x += 1
                    if pin_x >= self.pack_maker_params["col_num"]:
                        pin_x = 0
                        pin_y += 1
                    counter += 1
                    if counter >= counter_max:
                        canvas.save(
                            os.path.join(
                                output_dir,
                                target_dir
                                + str(big_pic_counter)
                                + self.name_extension
                                + str(counter)
                                + "total"
                                + ".jpg",
                            )
                        )

                        canvas = PIL.Image.new(
                            "RGB",
                            (
                                self.pack_maker_params["col_num"] * self.card_size[0],
                                self.pack_maker_params["row_num"] * self.card_size[1],
                            ),
                            (255, 255, 255),
                        )
                        big_pic_counter += 1
                        counter = 0
                        pin_x = 0
                        pin_y = 0
        if counter != 0:
            canvas.save(
                os.path.join(
                    output_dir,
                    target_dir
                    + str(big_pic_counter)
                    + self.name_extension
                    + str(counter)
                    + "total"
                    + ".jpg",
                )
            )

            canvas = PIL.Image.new(
                "RGB",
                (
                    self.pack_maker_params["col_num"] * self.card_size[0],
                    self.pack_maker_params["row_num"] * self.card_size[1],
                ),
                (255, 255, 255),
            )
            big_pic_counter += 1
            counter = 0
            pin_x = 0
            pin_y = 0

    def make_all_cards(self):
        if (
            os.path.exists(self.pack_maker_params["all_cards_output_dir"])
            and not self.pack_maker_params["overwrite"]
        ):
            print("all_cards_output_dir already exists, skip")
            return
        if not os.path.exists(self.pack_maker_params["all_cards_output_dir"]):
            os.makedirs(self.pack_maker_params["all_cards_output_dir"])

        for type_dir in os.listdir(self.pack_maker_params["all_cards_dir"]):
            if not os.path.isdir(
                os.path.join(self.pack_maker_params["all_cards_dir"], type_dir)
            ):
                continue
            self.make_all_cards_from_dir(
                os.path.join(self.pack_maker_params["all_cards_dir"], type_dir),
                type_dir,
            )

    def deck_analyze(self, card_nums):
        type_count = {
            "英雄": 0,
            "生物": 0,
            "道具": 0,
            "技能": 0,
            "衍生物": 0,
            "主卡组": 0,
            "技能卡组": 0,
            "衍生卡组": 0,
            "无": 0,
            "火": 0,
            "水": 0,
            "气": 0,
            "地": 0,
            "光": 0,
            "暗": 0,
        }
        valid = True
        card_count = {}
        for card_num in card_nums:
            if card_num == "//":
                continue

            if card_num[0] == "4":
                type_count["英雄"] += 1
            elif card_num[0] == "1":
                type_count["生物"] += 1
            elif card_num[0] == "2":
                type_count["道具"] += 1
            elif card_num[0] == "3":
                type_count["技能"] += 1

            if card_num[1] == "0":
                type_count["无"] += 1
            elif card_num[1] == "1":
                type_count["火"] += 1
            elif card_num[1] == "2":
                type_count["水"] += 1
            elif card_num[1] == "3":
                type_count["气"] += 1
            elif card_num[1] == "4":
                type_count["地"] += 1
            elif card_num[1] == "5":
                type_count["光"] += 1
            elif card_num[1] == "6":
                type_count["暗"] += 1

            if card_num not in card_count.keys():
                card_count[card_num] = 1
            else:
                card_count[card_num] += 1
            if card_num[2] != "0" and card_count[card_num] > int(card_num[2]):
                print("card_num: ", card_num, " excceed limit")
                valid = False
            if (card_num[0] == "1" or card_num[0] == "2") and card_num[2] != "0":
                type_count["主卡组"] += 1
            elif card_num[0] == "3" and card_num[2] != "0":
                type_count["技能卡组"] += 1
            elif card_num[2] == "0":
                type_count["衍生卡组"] += 1
        print("DECK COMPOSITION: ", type_count)
        if type_count["主卡组"] != 30 or type_count["技能卡组"] != 12:
            valid = False
        if not valid:
            print("DECK NOT VALID, please rebuild your deck")
        else:
            print("DECK VALID")

    def make_single_deck(self):
        if (
            os.path.exists(self.pack_maker_params["single_deck_output_dir"])
            and not self.pack_maker_params["overwrite"]
        ):
            print("single_deck_output_dir already exists, skip")
            return
        if not os.path.exists(self.pack_maker_params["single_deck_output_dir"]):
            os.makedirs(self.pack_maker_params["single_deck_output_dir"])
        single_deck_card_nums = []
        with open(self.pack_maker_params["deck_txt_path"], "r", encoding="utf-8") as f:
            for line in f.readlines():
                card_num = line.strip()
                if card_num == "":
                    continue
                if card_num.startswith("#"):
                    continue
                elif card_num.startswith("//"):
                    single_deck_card_nums.append("//")
                elif card_num in self.all_card_path_dict.keys():
                    single_deck_card_nums.append(card_num)
                else:
                    print("card not found: ", card_num)
        self.deck_analyze(single_deck_card_nums)
        deck_name = os.path.basename(self.pack_maker_params["deck_txt_path"]).split(
            "."
        )[-2]
        canvas = PIL.Image.new(
            "RGB",
            (
                self.pack_maker_params["col_num"] * self.card_size[0],
                self.pack_maker_params["row_num"] * self.card_size[1],
            ),
            (255, 255, 255),
        )
        pin_x = 0
        pin_y = 0
        counter = 0
        counter_max = (
            self.pack_maker_params["col_num"] * self.pack_maker_params["row_num"]
        )
        big_pic_counter = 0

        for card_num in tqdm(single_deck_card_nums):
            if card_num == "//":
                if counter != 0:
                    canvas.save(
                        os.path.join(
                            self.pack_maker_params["single_deck_output_dir"],
                            deck_name
                            + str(big_pic_counter)
                            + self.name_extension
                            + str(counter)
                            + "total"
                            + ".jpg",
                        )
                    )

                canvas = PIL.Image.new(
                    "RGB",
                    (
                        self.pack_maker_params["col_num"] * self.card_size[0],
                        self.pack_maker_params["row_num"] * self.card_size[1],
                    ),
                    (255, 255, 255),
                )
                big_pic_counter += 1
                counter = 0
                pin_x = 0
                pin_y = 0
                continue
            card_file = self.all_card_path_dict[card_num]
            if (
                card_file.endswith(".jpg")
                or card_file.endswith(".png")
                or card_file.endswith(".jpeg")
            ):
                target_image = PIL.Image.open(card_file).convert("RGB")
                canvas.paste(
                    target_image,
                    (
                        pin_x * self.card_size[0],
                        pin_y * self.card_size[1],
                    ),
                )
                pin_x += 1
                if pin_x >= self.pack_maker_params["col_num"]:
                    pin_x = 0
                    pin_y += 1
                counter += 1
                if counter >= counter_max:
                    canvas.save(
                        os.path.join(
                            self.pack_maker_params["single_deck_output_dir"],
                            deck_name
                            + str(big_pic_counter)
                            + self.name_extension
                            + str(counter)
                            + "total"
                            + ".jpg",
                        )
                    )

                    canvas = PIL.Image.new(
                        "RGB",
                        (
                            self.pack_maker_params["col_num"] * self.card_size[0],
                            self.pack_maker_params["row_num"] * self.card_size[1],
                        ),
                        (255, 255, 255),
                    )
                    big_pic_counter += 1
                    counter = 0
                    pin_x = 0
                    pin_y = 0

        if counter != 0:
            canvas.save(
                os.path.join(
                    self.pack_maker_params["single_deck_output_dir"],
                    deck_name
                    + str(big_pic_counter)
                    + self.name_extension
                    + str(counter)
                    + "total"
                    + ".jpg",
                )
            )

            canvas = PIL.Image.new(
                "RGB",
                (
                    self.pack_maker_params["col_num"] * self.card_size[0],
                    self.pack_maker_params["row_num"] * self.card_size[1],
                ),
                (255, 255, 255),
            )
            big_pic_counter += 1
            counter = 0
            pin_x = 0
            pin_y = 0

    def make_pack(self):
        if self.pack_maker_params["make_all_cards"]:
            self.make_all_cards()
        if self.pack_maker_params["make_single_deck"]:
            self.make_single_deck()

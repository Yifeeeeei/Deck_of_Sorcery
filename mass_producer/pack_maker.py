import PIL.Image
import json
import os
from tqdm import tqdm


class PackMaker:
    def __init__(self, pack_maker_params_path: str):
        self.pack_maker_params = dict(
            json.load(open(pack_maker_params_path, "r", encoding="utf-8"))
        )
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
                                self.pack_maker_params["all_cards_output_dir"],
                                target_dir,
                                target_dir + str(big_pic_counter) + ".jpg",
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
                    self.pack_maker_params["all_cards_output_dir"],
                    target_dir,
                    target_dir + str(big_pic_counter) + ".jpg",
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
        with open(self.pack_maker_params["deck_txt_path"], "r") as f:
            for line in f.readlines():
                card_num = line.strip()
                if card_num.startswith("#"):
                    continue
                if card_num in self.all_card_path_dict.keys():
                    single_deck_card_nums.append(card_num)
                else:
                    print("card not found: ", card_num)
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
                            deck_name + str(big_pic_counter) + ".jpg",
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
                    deck_name + str(big_pic_counter) + ".jpg",
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

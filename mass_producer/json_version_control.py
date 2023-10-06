import json
import os
import shutil


class JsonVersionController:
    def __init__(self, new_json_path):
        self.new_json_path = new_json_path
        self.old_json_path = None
        self.get_old_json_path()
        new_json_dict = dict(self.get_json())
        # copy old json to new json if new json != old json
        if (
            self.old_json_path is not None
            and "use_former_version" in new_json_dict
            and new_json_dict["use_former_version"]
        ):
            self.copy_old_json_to_new_json()
        # save the version
        target_path = os.path.join("back_up", os.path.basename(self.new_json_path))
        self.copy_new_json_to_path(target_path)

    def copy_old_json_to_new_json(self):
        new_json_dict = dict(self.get_json())
        old_json_dict = dict(json.load(open(self.old_json_path, "r", encoding="utf-8")))
        if "use_former_version" in new_json_dict:
            old_json_dict["use_former_version"] = new_json_dict["use_former_version"]
        if "@use_former_version" in new_json_dict:
            old_json_dict["@use_former_version"] = new_json_dict["@use_former_version"]
        json.dump(
            old_json_dict,
            open(self.new_json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )

    def copy_new_json_to_path(self, path):
        if not os.path.exists("back_up"):
            os.makedirs("back_up")
        # shutil.copy(self.new_json_path, path)
        new_json_dict = dict(self.get_json())
        if "use_former_version" in new_json_dict:
            del new_json_dict["use_former_version"]
        if "@use_former_version" in new_json_dict:
            del new_json_dict["@use_former_version"]
        json.dump(
            new_json_dict,
            open(path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )

    def get_old_json_path(self):
        json_file_name = os.path.basename(self.new_json_path)
        tmp_old_json_path = os.path.join("back_up", json_file_name)
        if os.path.exists(tmp_old_json_path):
            self.old_json_path = tmp_old_json_path
        else:
            self.old_json_path = None

    def get_json(self):
        return json.load(open(self.new_json_path, "r", encoding="utf-8"))

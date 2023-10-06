import json
import os
import shutil


class JsonVersionController:
    def __init__(self, new_json_path):
        self.new_json_path = new_json_path
        self.old_json_path = None
        self.get_old_json_path()

        # copy old json to new json if new json != old json
        if self.old_json_path is not None:
            new_json = json.load(open(self.new_json_path, "r", encoding="utf-8"))
            old_json = json.load(open(self.old_json_path, "r", encoding="utf-8"))
            if new_json != old_json:
                self.copy_old_json_to_new_json()
        # save the version
        target_path = os.path.join("back_up", os.path.basename(self.new_json_path))
        self.copy_new_json_to_path(target_path)

    def copy_old_json_to_new_json(self):
        shutil.copy(self.old_json_path, self.new_json_path)

    def copy_new_json_to_path(self, path):
        if not os.path.exists("back_up"):
            os.makedirs("back_up")
        shutil.copy(self.new_json_path, path)

    def get_old_json_path(self):
        json_file_name = os.path.basename(self.new_json_path)
        tmp_old_json_path = os.path.join("back_up", json_file_name)
        if os.path.exists(tmp_old_json_path):
            self.old_json_path = tmp_old_json_path
            old_json = json.load(open(self.old_json_path, "r", encoding="utf-8"))
            old_json = dict(old_json)
            if (
                "use_former_version" in old_json
                and old_json["use_former_version"] == True
            ):
                self.old_json_path = tmp_old_json_path
            else:
                self.old_json_path = None
        else:
            self.old_json_path = None

    def get_json(self):
        return json.load(open(self.new_json_path, "r", encoding="utf-8"))

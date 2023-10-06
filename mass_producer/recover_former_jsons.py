from json_version_control import JsonVersionController

if __name__ == "__main__":
    list_of_files = [
        "mass_producer_params_xlsx.json",
        "single_card_maker_params.json",
        "pack_maker_params.json",
    ]
    for json_file in list_of_files:
        json_verson_controller = JsonVersionController(json_file)

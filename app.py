import eel
import json

SETTING_FILE_RELATIVE_PATH: str = "setting/setting.json"


def main(window_width: int, window_height: int, port: int):
    eel.init("web")
    eel.start("hello.html", size=(window_width, window_height), port=port)


if __name__ == "__main__":
    with open("setting/setting.json", "r") as setting_file:
        setting_data = json.load(setting_file)
        window_width = setting_data["width"]
        window_height = setting_data["height"]
        port = setting_data["port"]
    main(window_width=window_width, window_height=window_height, port=port)

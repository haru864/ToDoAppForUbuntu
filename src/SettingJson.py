from typing import Optional
import json
import inspect


class SettingJson:
    max_num_of_tasks: int = None
    beep_period_seconds: int = None
    sound_file: str = None

    @classmethod
    def loadSettingJson(cls) -> None:
        try:
            with open("setting/setting.json", "r") as confJsonRead:
                data = json.load(confJsonRead)
                SettingJson.max_num_of_tasks = data["max_num_of_tasks"]
                SettingJson.beep_period_seconds = data["beep_period_seconds"]
                SettingJson.sound_file = data["sound_file"]
        except Exception as e:
            print(f"{cls}.{inspect.currentframe().f_code.co_name}: {e}")
            raise e

    @classmethod
    def updateSettingJson(cls) -> None:
        try:
            with open("setting/setting.json", "w") as confJsonWrite:
                json.dump(SettingJson.__generateDict(), confJsonWrite)
        except Exception as e:
            print(f"{cls}.{inspect.currentframe().f_code.co_name}: {e}")
            raise e

    @classmethod
    def changeSetting(
        cls,
        new_max_num_of_tasks: Optional[int],
        new_beep_period_seconds: Optional[int],
        new_sound_file: Optional[str],
    ) -> None:
        if new_max_num_of_tasks is not None:
            SettingJson.max_num_of_tasks = new_max_num_of_tasks
        if new_beep_period_seconds is not None:
            SettingJson.beep_period_seconds = new_beep_period_seconds
        if new_sound_file is not None:
            SettingJson.sound_file = new_sound_file

    @classmethod
    def __generateDict(cls) -> dict:
        data = {}
        data["max_num_of_tasks"] = SettingJson.max_num_of_tasks
        data["beep_period_seconds"] = SettingJson.beep_period_seconds
        data["sound_file"] = SettingJson.sound_file
        return data

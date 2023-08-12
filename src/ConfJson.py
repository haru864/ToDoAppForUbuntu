from typing import Optional
from Setting import Setting
import json


class ConfJson:
    def __init__(self) -> None:
        self.max_num_of_tasks: int = None
        self.beep_period_seconds: int = None
        self.sound_file: str = None
        self.loadConfJsonFile()

    def loadConfJsonFile(self) -> None:
        try:
            with open("setting/conf.json", "r") as confJsonRead:
                data = json.load(confJsonRead)
                self.max_num_of_tasks: int = data["max_num_of_tasks"]
                self.beep_period_seconds: int = data["beep_period_seconds"]
                self.sound_file: str = data["sound_file"]
        except Exception as e:
            print(f"ConfJson.loadConfJsonFile(): {e}")
            raise e

    def updateConfJsonFileBySetting(self) -> None:
        try:
            self.max_num_of_tasks: int = Setting.MAX_NUM_OF_TASKS
            self.beep_period_seconds: int = Setting.BEEP_PERIOD_SECONDS
            self.sound_file: str = Setting.SOUND_FILE
            with open("setting/conf.json", "w") as confJsonWrite:
                json.dump(self.__generateDict(), confJsonWrite)
        except Exception as e:
            print(f"ConfJson.reflectSetting(): {e}")
            raise e

    def __generateDict(self) -> dict:
        data = {}
        data["max_num_of_tasks"] = self.max_num_of_tasks
        data["beep_period_seconds"] = self.beep_period_seconds
        data["sound_file"] = self.sound_file
        return data

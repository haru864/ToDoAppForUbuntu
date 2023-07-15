import os


class ConfJson:
    def __init__(
        self,
        max_num_of_tasks: str,
        beep_period_seconds: str,
        default_task_time: str,
        sound_file: str,
    ) -> None:
        self.max_num_of_tasks: str = max_num_of_tasks
        self.beep_period_seconds: str = beep_period_seconds
        self.default_task_time: str = default_task_time
        self.sound_file: str = sound_file
        errMsgList = self.validate()
        if len(errMsgList) != 0:
            raise Exception(errMsgList)

    def validate(self) -> list:
        errMsgList = []
        if self.max_num_of_tasks.isdigit() is False:
            errMsgList.append("MAX_NUM_OF_TASKS must be digit")
        if self.beep_period_seconds.isdigit() is False:
            errMsgList.append("BEEP_PERIOD_SECONDS must be digit")
        if self.default_task_time.isdigit() is False:
            errMsgList.append("DEFAULT_TASK_TIME must be digit")
        if os.path.isfile(self.sound_file) is False:
            errMsgList.append("SOUND_FILE must be existing file")
        if self.sound_file.endswith(".ogg") is False:
            errMsgList.append("SOUND_FILE must be ogg file")
        return errMsgList

    def loadConfJson(self):
        pass

    def generateDict(self) -> dict:
        data = {}
        data["max_num_of_tasks"] = int(self.max_num_of_tasks)
        data["beep_period_seconds"] = int(self.beep_period_seconds)
        data["default_task_time"] = int(self.default_task_time)
        data["sound_file"] = self.sound_file
        return data

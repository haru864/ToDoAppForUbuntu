from typing import Optional
import os


class Setting:
    MAX_NUM_OF_TASKS: int = None
    BEEP_PERIOD_SECONDS: int = None
    DEFAULT_TASK_TIME: int = None
    SOUND_FILE: str = None

    @classmethod
    def updateSetting(
        self,
        newMaxNumOfTasks: int = None,
        newBeepPeriodSeconds: int = None,
        newDefaultTaskTime: int = None,
        newSoundFile: str = None,
    ) -> None:
        errMsgList = Setting.__validateSettingValue(
            newMaxNumOfTasks=newMaxNumOfTasks,
            newBeepPeriodSeconds=newBeepPeriodSeconds,
            newDefaultTaskTime=newDefaultTaskTime,
            newSoundFile=newSoundFile,
        )
        if errMsgList is not None:
            raise Exception(errMsgList)
        if newMaxNumOfTasks is not None:
            Setting.MAX_NUM_OF_TASKS = newMaxNumOfTasks
        if newBeepPeriodSeconds is not None:
            Setting.BEEP_PERIOD_SECONDS = newBeepPeriodSeconds
        if newDefaultTaskTime is not None:
            Setting.DEFAULT_TASK_TIME = newDefaultTaskTime
        if newSoundFile is not None:
            Setting.SOUND_FILE = newSoundFile

    @classmethod
    def __validateSettingValue(
        cls,
        newMaxNumOfTasks: Optional[int | None],
        newBeepPeriodSeconds: Optional[int | None],
        newDefaultTaskTime: Optional[int | None],
        newSoundFile: Optional[str | None],
    ) -> Optional[list[str] | None]:
        errMsgList = []
        if (
            newMaxNumOfTasks is not None
            and Setting.__isPositiveDecimal(newMaxNumOfTasks) is False
        ):
            errMsgList.append("MAX_NUM_OF_TASKS must be digit")
        if (
            newBeepPeriodSeconds is not None
            and Setting.__isPositiveDecimal(newBeepPeriodSeconds) is False
        ):
            errMsgList.append("BEEP_PERIOD_SECONDS must be digit")
        if (
            newDefaultTaskTime is not None
            and Setting.__isPositiveDecimal(newDefaultTaskTime) is False
        ):
            errMsgList.append("DEFAULT_TASK_TIME must be digit")
        if newSoundFile is not None and os.path.isfile(newSoundFile) is False:
            errMsgList.append("SOUND_FILE must be existing file")
        if newSoundFile is not None and newSoundFile.endswith(".ogg") is False:
            errMsgList.append("SOUND_FILE must be OGG")
        return None if len(errMsgList) == 0 else errMsgList

    @classmethod
    def __isPositiveDecimal(self, number: int) -> bool:
        return number > 0 and str(number).isdigit()

from MainWindow import MainWindow
from ConfJson import ConfJson
from Setting import Setting


def centerWindow(window) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def main():
    # 設定ファイル読み込み
    confJson = ConfJson()
    Setting.updateSetting(
        newMaxNumOfTasks=confJson.max_num_of_tasks,
        newBeepPeriodSeconds=confJson.beep_period_seconds,
        newDefaultTaskTime=confJson.default_task_time,
        newSoundFile=confJson.sound_file,
    )

    # メインウィンドウを生成
    mainWIndow = MainWindow()

    # メインウィンドウを表示
    mainWIndow.mainloop()


if __name__ == "__main__":
    main()

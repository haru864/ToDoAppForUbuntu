from MainWindow import MainWindow
from SettingJson import SettingJson


def centerWindow(window) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def main():
    # 設定ファイル読み込み
    SettingJson.loadSettingJson()

    # メインウィンドウを生成
    mainWIndow = MainWindow()

    # メインウィンドウを表示
    mainWIndow.mainloop()


if __name__ == "__main__":
    main()

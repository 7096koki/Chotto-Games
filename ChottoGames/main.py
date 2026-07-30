import importlib
import time
import subprocess
import os
import sys
# 元のパス（libフォルダなどを見つける用）
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lib import screen, score, controls


def menu():
    cursor_pos = 0

    # 1つの辞書に完全統合！
    game_list = {
        "guess_number": {"current_level": 1, "max_level": 255},
        "minesweeper": {"current_level": 1, "max_level": 5},
        "sneak": {"current_level": 1, "max_level": 9},
    }

    while True:
        while True:
            # 現在選択中のゲーム名（"guess_number"等）と設定データ（辞書）を取得
            game_key = list(game_list.keys())[cursor_pos]
            select_game = game_list[game_key]
            level = select_game["current_level"]

            screen.clear(1)

            print("\033[1m==============================\033[0m")
            print("\033[1m   Welcome to Chotto-Games!   \033[0m")
            print("\033[1m==============================\033[0m\n")
            print("====MENU============================")
            for i, show_game in enumerate(game_list):
                if cursor_pos == i:
                    print(
                        f"\033[44:7m{show_game}\033[0m"
                    )  # 選択中のゲームをハイライト表示
                else:
                    print(f"\033[34m{show_game}\033[0m")

            print("-----------------------------------")
            print(f"Level: {level}")

            # キー入力を受け付ける
            match controls.readkey():
                case "UP":
                    cursor_pos = max(0, cursor_pos - 1)
                case "DOWN":
                    cursor_pos = min(len(game_list) - 1, cursor_pos + 1)
                case "ENTER":
                    # 選択決定！そのままループを抜ける
                    break
                case "RIGHT":
                    # 現在のゲームのレベルを上げる
                    select_game["current_level"] = min(
                        select_game["max_level"], level + 1
                    )
                case "LEFT":
                    # 現在のゲームのレベルを下げる
                    select_game["current_level"] = max(1, level - 1)
                case "i" | "I":
                    # インフォメーション機能
                    print("\033[92m====INFOMATION==============")
                    print("----GAME DETAIL---------")
                    try:
                        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                        game_path = os.path.join(
                            BASE_DIR, "games", f"{game_key}.py"
                        )

                        spec = importlib.util.spec_from_file_location(
                            game_key, game_path
                        )
                        game_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(game_module)

                        if hasattr(game_module, "INFO"):
                            info = game_module.INFO
                            print(f"RULE     : {info.get('rule', 'None')}")
                            print(f"CONTROLS : {info.get('controls', 'None')}")
                    except Exception as ex:
                        print(f"READ ERROR: {ex}")

                    # ランキングを表示する
                    print("\n----RANKING-------------")
                    ranking = score.load(game_key, level)
                    if ranking != []:
                        for i, record in enumerate(ranking):
                            if i < 9:
                                print(f" {i + 1}. {record}")
                            else:
                                print(f"{i + 1}. {record}")
                    else:
                        print("Not found\033")

                    print("\033[0m", end="")
                    controls.readkey()
                case _:
                    pass

        screen.clear(1)

        print(f"===={game_key}============================")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(BASE_DIR, "games", f"{game_key}.py")

        time.sleep(1.0)  # ゲーム開始前のまたーりタイム

        # ゲームを実行する
        try:
            exec_game_proc = subprocess.Popen(
                ["python3", "-u", game_path, str(level)],
                stderr=subprocess.DEVNULL,
            )
            exec_game_proc.wait()
        except KeyboardInterrupt:
            exec_game_proc.terminate()
        
        # ▼ ゲーム終了直後にターミナルを綺麗に掃除！ ▼
        print("\033[0m\r", end="", flush=True)
        screen.clear(1)

        if sys.platform != "win32":
            os.system("stty sane")  # Mac/Linuxの端末モードを初期状態に強制復元！


# 実行するやつコーナー
screen.clear(1)
menu()
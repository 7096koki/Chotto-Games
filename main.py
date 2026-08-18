import importlib.util
import os
import subprocess
import sys
import time

# 元のパス（libフォルダなどを見つける用）
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lib import controls, score, screen, ui


def load_game_info(game_key: str) -> dict:
    """games/{game_key}.py から INFO 辞書を読み込むヘルパー関数"""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(BASE_DIR, "games", f"{game_key}.py")

        spec = importlib.util.spec_from_file_location(game_key, game_path)
        if spec and spec.loader:
            game_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(game_module)
            if hasattr(game_module, "INFO"):
                return getattr(game_module, "INFO")
    except Exception:
        pass
    return {}


def menu():
    cursor_pos = 0

    # gamesフォルダから自動的にゲームリストとmax_levelを取得！
    # 先頭が _ や __ のファイル（WIPや内部用）は自動除外
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    games_dir = os.path.join(BASE_DIR, "games")

    game_list = {}
    if os.path.exists(games_dir):
        # アルファベット順でソートして読み込み
        for filename in sorted(os.listdir(games_dir)):
            if filename.endswith(".py") and not filename.startswith(
                ("_", "__")
            ):
                g_key = filename[:-3]  # ".py" を除去
                info = load_game_info(g_key)
                max_lvl = info.get("max_level", 1)
                game_list[g_key] = {"current_level": 1, "max_level": max_lvl}

    # 万が一ゲームが1つも見つからなかった場合のフォールバック（画面クラッシュ防止）
    if not game_list:
        raise AttributeError("Game_list wo shutoku dekimasendeshita.\nsaikidou suru ka github issue kara otoiawasekudasai.")

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
            print(ui.draw_line("d", "l", "MENU"))
            for i, show_game in enumerate(game_list):
                if cursor_pos == i:
                    print(
                        f"\033[44:7m{show_game}\033[0m"
                    )  # 選択中のゲームをハイライト表示
                else:
                    print(f"\033[34m{show_game}\033[0m")

            print(ui.draw_line("s", "l"))
            print(f"Level: {level}")

            # キー入力を受け付ける
            match controls.readkey():
                case "UP":
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        # 上下キーで違うゲームを選択すると1にリセット！
                        new_key = list(game_list.keys())[cursor_pos]
                        game_list[new_key]["current_level"] = 1

                case "DOWN":
                    if cursor_pos < len(game_list) - 1:
                        cursor_pos += 1
                        # 上下キーで違うゲームを選択すると1にリセット！
                        new_key = list(game_list.keys())[cursor_pos]
                        game_list[new_key]["current_level"] = 1

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
                    print("\033[92m", end="")
                    print(ui.draw_line("d", "m", "INFOMATION"))
                    print(ui.draw_line("s", "s", "GAME_DETAIL"))
                    try:
                        info = load_game_info(game_key)
                        if info:
                            print(f"RULE     : {info.get('rule', 'None')}")
                            print(
                                f"CONTROLS : {info.get('controls', 'None')}"
                            )
                        else:
                            print("RULE     : None")
                            print("CONTROLS : None")
                    except Exception as ex:
                        print(f"READ ERROR: {ex}")

                    # ランキングを表示する
                    print()
                    print(ui.draw_line("s", "s", "RANKING"))
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

        screen.clear(1)


# 実行するやつコーナー
screen.clear(1)
menu()
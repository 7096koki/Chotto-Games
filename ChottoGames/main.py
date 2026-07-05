import importlib
import time
import subprocess
import os
import sys
import readchar
# 元のパス（libフォルダなどを見つける用）
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lib import screen
from lib import score


def menu():
    cursor_pos = 0

    game_list = ["guess_number", "minesweeper", "reversi"]
    game_level_list = {
        "guess_number": 255,
        "minesweeper": 6,
        "reversi": 1
    }
    current_level_list = {
        "guess_number": 1,
        "minesweeper": 1,
        "reversi": 1
    }

    while True: 
        while True:
            select_game = game_list[cursor_pos]
            level = current_level_list[select_game]
    
            screen.clear()
            print("Welcome to ChottoGames!")
            print("====MENU============================")
            for i, show_game in enumerate(game_list):
                if cursor_pos == i:
                    print("\033[7m" + show_game + "\033[0m")  # 選択中のゲームの表示
                else:
                    print(show_game)
            
            print(f"Level: {level}")

            # キー入力を受け付ける
            match readchar.readkey():
                case readchar.key.UP:
                    cursor_pos = max(0, cursor_pos - 1)
                case readchar.key.DOWN:
                    cursor_pos = min(len(game_list) - 1, cursor_pos + 1)
                case readchar.key.ENTER:
                    select_game = game_list[cursor_pos]
                    break
                case readchar.key.RIGHT:
                    current_level_list[select_game] = min(game_level_list[game_list[cursor_pos]], level + 1)
                case readchar.key.LEFT:
                    current_level_list[select_game] = max(1, level - 1)
                case "i" | "I":
                    # インフォメーション機能
                    try:
                        # 確実に games フォルダの中のファイルを絶対パスで指定する
                        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                        game_path = os.path.join(
                            BASE_DIR, "games", f"{select_game}.py"
                        )

                        # ファイルパスから直接モジュールを読み込む魔法
                        spec = importlib.util.spec_from_file_location(
                            select_game, game_path
                        )
                        game_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(game_module)

                        # ゲーム側に INFO が定義されていたら表示する
                        if hasattr(game_module, "INFO"):
                            info = game_module.INFO
                            print(f"[rule]   : {info.get('rule', 'None')}")
                            print(f"[controls] : {info.get('controls', 'None')}")
                    except Exception as e:
                        # 何のエラーが出ているか画面に出すようにして原因を突き止めやすくする
                        print(f"READ ERROR: {e}")

                    # ランキングを表示する
                    print("\n----RANKING-------------")
                    ranking = score.load(select_game, level)
                    if ranking != []:
                        for i, record in enumerate(ranking):
                            print(f"{i}. {record}")
                    else:
                        print("Not found")
                    readchar.readkey()
                case _:
                    pass

        screen.clear()

        print(f"===={select_game}============================")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(BASE_DIR, "games", f"{select_game}.py")

        time.sleep(1.0) # ゲーム開始前のまたーりタイム

        # ゲームを実行する
        try:
            exec_game_proc = subprocess.Popen(["python3", "-u", game_path, str(level)], stderr=subprocess.DEVNULL)
            # ゲームが終わるまで待つ
            exec_game_proc.wait()
        except KeyboardInterrupt:
            # Ctrl+Cで強制終了された場合
            exec_game_proc.terminate()
        
        print()


menu()

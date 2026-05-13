import subprocess
import os
import readchar
import time

def menu():
    cursor_pos = 0

    game_list = ["guess_number", "minesweeper"]
    game_level_list = {
        "guess_number": 16,
        "minesweeper": 5
    }
    current_level_list = {
        "guess_number": 1,
        "minesweeper": 1
    }

    print("Welcome to ChottoGames!")

    while True: 
        while True:
            select_game = game_list[cursor_pos]
            level = current_level_list[select_game]
    
            os.system("clear")
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
                case _:
                    pass

        os.system("clear")

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

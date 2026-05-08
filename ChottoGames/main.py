import subprocess
import os

def menu():
    game_list = ["guess_number", "mainsweeper"]
    print("Welcome to ChottoGames!")

    while True:
        print("====MENU============================")
        for n, show_name in enumerate(game_list, 0):
            print(f"{n}. {show_name}")

        select = input("game number: ")
        
        try:
            select = int(select)
        except ValueError:
            print("not found")
            continue
        
        if select < 0 or select >= len(game_list):
            print("not found")
            continue
        
        print(f"===={game_list[select]}============================")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(BASE_DIR, "games", f"{game_list[select]}.py")

        # ゲームを実行する
        try:
            exec_game_proc = subprocess.Popen(["python3", game_path], stderr=subprocess.DEVNULL)
            # ゲームが終わるまで待つ
            exec_game_proc.wait()
        except KeyboardInterrupt:
            # Ctrl+Cで強制終了された場合
            exec_game_proc.terminate()
            print() # ^Cが上のゲームリストに影響しないようにするため


menu()

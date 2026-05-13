import random
import readchar
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import score

# カーソルの初期位置
y = 0
x = 0

# 難易度設定
level = int(sys.argv[1])

match level:
    case 1:
        size = 9
        bomb = 10
    case 2:
        size = 16
        bomb = 40
    case 3:
        size = 22
        bomb = 99
    case 4:
        size = 27
        bomb = 99
    case 5:
        size = 27
        bomb = 667
    case _:
        size = 9
        bomb = 10

#ステージを作る
data_stage = [[0 for _ in range(size)] for _ in range(size)]
display_stage = [["□" for _ in range(size)] for _ in range(size)]

cell_color = {
    0: "\x1b[90m.\x1b[0m",
    1: "\x1b[38;5;33m1\x1b[0m",    # DodgerBlue
    2: "\x1b[38;5;82m2\x1b[0m",    # Chartreuse
    3: "\x1b[38;5;196m3\x1b[0m",   # Red
    4: "\x1b[38;5;27m4\x1b[0m",    # Blue
    5: "\x1b[38;5;124m5\x1b[0m",   # Red3
    6: "\x1b[38;5;45m6\x1b[0m",    # Turquoise
    7: "\x1b[38;5;15m7\x1b[0m",    # White (黒だと見えないため)
    8: "\x1b[38;5;250m8\x1b[0m",   # Grey
    "*": "*",
    "F": "\x1b[38;5;226mF\x1b[0m", # 黄色(226)で見やすく
    "□": "\x1b[38;5;242m□\x1b[0m"  # 少し明るめの枠線
}

# 爆弾を置く
count_bomb = 0

while count_bomb != bomb:
    put_x = random.randint(0, size - 1)
    put_y = random.randint(0, size - 1)

    if data_stage[put_y][put_x] != "*":
        data_stage[put_y][put_x] = "*"
        count_bomb += 1
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny, nx = put_y + dy, put_x + dx
                
                if 0 <= ny < size and 0 <= nx < size:
                    if data_stage[ny][nx] != "*":
                        data_stage[ny][nx] += 1
    else:
        continue

# タイマー変数
start_time = None

def timer_start():
    global start_time
    start_time = time.time()

def open_cell(oy, ox):
    if not (0 <= oy < size and 0 <= ox < size):
        return

    if display_stage[oy][ox] != "□":
        return

    display_stage[oy][ox] = data_stage[oy][ox]

    if data_stage[oy][ox] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                open_cell(oy + dy, ox + dx)

def show_stage():
    os.system("clear")
    for sy in range(size):
        for sx in range(size):
            cell = display_stage[sy][sx]
            colored_cell = cell_color.get(cell, str(cell))

            if sy == y and sx == x:
                print(f"\033[7m{colored_cell}\033[0m", end=" ")
            else:
                print(colored_cell, end=" ")

        print()

def game_over():
    for sy in range(size):
        for sx in range(size):
            answer_cell = data_stage[sy][sx]
            user_cell = display_stage[sy][sx]

            if answer_cell == "*": # 爆弾があるセル
                if user_cell == "F":
                    print(f"\033[33mF\033[0m", end=" ") # フラグが置いてある
                else:
                    print(f"\033[41m*\033[0m", end=" ") # フラグが置いていない
            elif user_cell == "F" and answer_cell != "*": # フラグミス
                print(f"\033[41m×\033[0m", end=" ")
            else:
                print(cell_color.get(answer_cell, str(answer_cell)), end=" ") # 通常表示

        print()
    print("Game Over!")
    

def main():
    global x, y, start_time, hit_bomb, remaining # 使うグローバル変数をまとめて宣言
    hit_bomb = 0 # 初期化
    remaining = size * size # 最初は全セルが閉じている

    while True:
        show_stage()
        print("-" * 40)
        print(f"Level {level} | ↑↓←→: Move | Enter: Open | F: Flag")
        if level == 4: print(f"Bombs Hit: {hit_bomb}") # レベル4なら被弾数表示
        print("-" * 40)

        key = readchar.readkey()

        match key:
            case readchar.key.DOWN:
                y = min(size - 1, y + 1)
            case readchar.key.UP:
                y = max(0, y - 1)
            case readchar.key.LEFT:
                x = max(0, x - 1)
            case readchar.key.RIGHT:
                x = min(size - 1, x + 1)
            case readchar.key.ENTER:
                if start_time is None:
                    timer_start()
                
                # 既に開いている場所やフラグの場所は何もしない
                if display_stage[y][x] != "□":
                    continue

                if data_stage[y][x] == "*":
                    if level == 4:
                        hit_bomb += 1
                        display_stage[y][x] = "*" # 爆弾を踏んだ印
                        continue
                    else:
                        game_over()
                        return False # 負けたらFalseを返す
                
                open_cell(y, x)
            case "f" | "F":
                if display_stage[y][x] == "□":
                    display_stage[y][x] = "F"
                elif display_stage[y][x] == "F":
                    display_stage[y][x] = "□"
            case _:
                continue

        # クリア判定
        remaining = 0
        for row in display_stage:
            remaining += row.count("□")
            remaining += row.count("F")

        if remaining == count_bomb:
            return True # クリアしたらTrueを返す

if __name__ == "__main__":
    # mainの結果を受け取る
    is_clear = main()
    
    # start_timeがNone（一度もEnterを押してない）場合の対策
    if start_time is None:
        start_time = time.time()

    stop_time = time.time() - start_time
    print(f"TIME: {stop_time:.3f}s")

    if is_clear:
        print("Game Clear!")
        if level != 4:
            score.save(level, float(f"{stop_time:.3f}"))
        else:
            # level 4の保存（hit_bombを渡す）
            score.save(level, float(f"{stop_time:.3f}"), user_data1=hit_bomb)
    
    print("Press any key to return to menu...")
    readchar.readkey() # input()よりreadkeyの方が「any key」感が出ます
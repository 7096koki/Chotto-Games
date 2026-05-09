import random
import readchar
import os
import time

# カーソルの初期位置
y = 0
x = 0

#ステージを作る
size = 9
data_stage = [[0 for _ in range(size)] for _ in range(size)]
display_stage = [["□" for _ in range(size)] for _ in range(size)]

cell_color = {
    0: "\033[90m.\033[0m",
    1: "\033[34m1\033[0m",
    2: "\033[32m2\033[0m",
    3: "\033[31m3\033[0m",
    4: "\033[35m4\033[0m",
    5: "\033[31m5\033[0m",
    6: "\033[36m6\033[0m",
    7: "\033[30m7\033[0m",
    8: "\033[37m8\033[0m",
    "*": "*",
    "F": "\033[33mF\033[0m",
    "□": "\033[90m□\033[0m"
}

# 爆弾を置く
total_bomb = 0

while total_bomb != 8:
    put_x = random.randint(0, size - 1)
    put_y = random.randint(0, size - 1)

    if data_stage[put_y][put_x] != "*":
        data_stage[put_y][put_x] = "*"
        total_bomb += 1
        
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
    global x, y

    while True:
        show_stage()

        # 操作説明
        print("-" * 40)
        print("↑↓←→: Move | Enter: Open | F: Flag")
        print("-" * 40)

        # キー入力を受け付ける
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
                if start_time is None: # 一手目からタイマー開始
                    timer_start()
                
                open_cell(y, x)
                if data_stage[y][x] == "*":
                    game_over()
                    break
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
        
        if remaining == total_bomb:
            print("Game Clear!")
            break


if __name__ == "__main__":
    main()
    print(f"TIME: {time.time() - start_time:.2f}s")
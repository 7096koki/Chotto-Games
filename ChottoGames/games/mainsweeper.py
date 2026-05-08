import random
import readchar
import sys
import os

#ステージを作る
size = 9
data_stage = [[0 for _ in range(size)] for _ in range(size)]
display_stage = [["□" for _ in range(size)] for _ in range(size)]

# 爆弾を置く
total_bomb = 0

# カーソルの初期位置
y = 0
x = 0

while total_bomb != 8:
    put_x = random.randint(0, size - 1)
    put_y = random.randint(0, size - 1)

    if data_stage[put_y][put_x] != "B":
        data_stage[put_y][put_x] = "B"
        total_bomb += 1
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny, nx = put_y + dy, put_x + dx
                
                if 0 <= ny < size and 0 <= nx < size:
                    if data_stage[ny][nx] != "B":
                        data_stage[ny][nx] += 1
    else:
        continue


def open_block(oy, ox):
    if not (0 <= oy < size and 0 <= ox < size):
        return

    if display_stage[oy][ox] != "□":
        return

    display_stage[oy][ox] = data_stage[oy][ox]

    if data_stage[oy][ox] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                open_block(oy + dy, ox + dx)

def show_stage():
    os.system("clear")
    for sy in range(size):
        for sx in range(size):
            if sy == y and sx == x:
                print("■", end="")
            else:
                print(display_stage[sy][sx], end="")

        print()

def main():
    global x, y

    while True:
        show_stage()

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
                open_block(y, x)
                if data_stage[y][x] == "B":
                    show_stage()
                    print("Game Over!")
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
    show_stage()
    main()
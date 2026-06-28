import os
import random
import sys
import time

import readchar

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import score, screen

INFO = {
    "title": "マインスイーパ",
    "rule": "80sからの定番PCゲーム。爆弾を避けて全部のマスを開けよう！",
    "controls": "↑↓←→: Move | Enter: Open | F: Flag",
}

# 状態を表す定数（マジックワードの共通化）
BOMB_MARK = "*" 
UNOPENED_MARK = "□"
FLAG_MARK = "F"

# カーソルの初期位置
y = 0
x = 0

# 難易度設定
LEVEL = int(sys.argv[1])

match LEVEL:
    case 1:
        SIZE = 9
        BOMB = 10
    case 2:
        SIZE = 16
        BOMB = 40
    case 3:
        SIZE = 22
        BOMB = 99
    case 4:
        SIZE = 27
        BOMB = 99
    case 5:
        SIZE = 27
        BOMB = 667
    case _:
        SIZE = 9
        BOMB = 10  # タイポ（bomb ➔ BOMB）を修正

# ステージを作る
data_stage = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
display_stage = [[UNOPENED_MARK for _ in range(SIZE)] for _ in range(SIZE)]

cell_color = {
    0: "\x1b[90m.\x1b[0m",
    1: "\x1b[38;5;33m1\x1b[0m",  # DodgerBlue
    2: "\x1b[38;5;82m2\x1b[0m",  # Chartreuse
    3: "\x1b[38;5;196m3\x1b[0m",  # Red
    4: "\x1b[38;5;27m4\x1b[0m",  # Blue
    5: "\x1b[38;5;124m5\x1b[0m",  # Red3
    6: "\x1b[38;5;45m6\x1b[0m",  # Turquoise
    7: "\x1b[38;5;15m7\x1b[0m",  # White
    8: "\x1b[38;5;250m8\x1b[0m",  # Grey
    BOMB_MARK: BOMB_MARK,
    FLAG_MARK: "\x1b[38;5;226mF\x1b[0m",  # 黄色
    UNOPENED_MARK: "\x1b[38;5;242m□\x1b[0m",  # 少し明るめの枠線
}

# 爆弾を置く
count_bomb = 0

while count_bomb != BOMB:
    put_x = random.randint(0, SIZE - 1)
    put_y = random.randint(0, SIZE - 1)

    if data_stage[put_y][put_x] != BOMB_MARK:
        data_stage[put_y][put_x] = BOMB_MARK
        count_bomb += 1

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny, nx = put_y + dy, put_x + dx

                if 0 <= ny < SIZE and 0 <= nx < SIZE:
                    if data_stage[ny][nx] != BOMB_MARK:
                        data_stage[ny][nx] += 1

# タイマー変数
start_time = None


def timer_start():
    global start_time
    start_time = time.time()


def open_cell(oy, ox):
    if not (0 <= oy < SIZE and 0 <= ox < SIZE):
        return

    if display_stage[oy][ox] != UNOPENED_MARK:
        return

    display_stage[oy][ox] = data_stage[oy][ox]

    if data_stage[oy][ox] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                open_cell(oy + dy, ox + dx)


def show_stage():
    screen.clear()
    for sy in range(SIZE):
        for sx in range(SIZE):
            cell = display_stage[sy][sx]
            colored_cell = cell_color.get(cell, str(cell))

            if sy == y and sx == x:
                print(f"\033[7m{colored_cell}\033[0m", end=" ")
            else:
                print(colored_cell, end=" ")
        print()


def game_over():
    for sy in range(SIZE):
        for sx in range(SIZE):
            answer_cell = data_stage[sy][sx]
            user_cell = display_stage[sy][sx]

            if answer_cell == BOMB_MARK:  # 爆弾があるセル
                if user_cell == FLAG_MARK:
                    print("\033[33mF\033[0m", end=" ")  # フラグが置いてある
                else:
                    print("\033[41m*\033[0m", end=" ")  # フラグが置いていない
            elif user_cell == FLAG_MARK and answer_cell != BOMB_MARK:  # フラグミス
                print("\033[41m×\033[0m", end=" ")
            else:
                print(cell_color.get(answer_cell, str(answer_cell)), end=" ")
        print()
    print("Game Over!")


def main():
    global x, y, start_time
    hit_bomb = 0  # ローカル変数として処理可能
    remaining = SIZE * SIZE
    input_history = []
    is_cheat = False

    while True:
        show_stage()
        print("-" * 40)
        print(f"LEVEL {LEVEL} | ↑↓←→: Move | Enter: Open | F: Flag")
        if LEVEL == 4:
            print(f"Bombs Hit: {hit_bomb}")
        print("-" * 40)

        if is_cheat and data_stage[y][x] == BOMB_MARK:
            print("#")

        key = readchar.readkey()

        if isinstance(key, str):
            input_history.append(key.lower())
            if len(input_history) > 5:
                input_history.pop(0)

        if "".join(input_history) == "xyzzy":
            is_cheat = True

        match key:
            case readchar.key.DOWN:
                y = min(SIZE - 1, y + 1)
            case readchar.key.UP:
                y = max(0, y - 1)
            case readchar.key.LEFT:
                x = max(0, x - 1)
            case readchar.key.RIGHT:
                x = min(SIZE - 1, x + 1)
            case readchar.key.ENTER:
                if start_time is None:
                    timer_start()

                # 既に開いている場所やフラグの場所は何もしない
                if display_stage[y][x] != UNOPENED_MARK:
                    continue

                if data_stage[y][x] == BOMB_MARK:
                    if LEVEL == 4:
                        hit_bomb += 1
                        display_stage[y][x] = BOMB_MARK  # 爆弾を踏んだ印
                        continue
                    else:
                        game_over()
                        return False, hit_bomb

                open_cell(y, x)
            case "f" | "F":
                if display_stage[y][x] == UNOPENED_MARK:
                    display_stage[y][x] = FLAG_MARK
                elif display_stage[y][x] == FLAG_MARK:
                    display_stage[y][x] = UNOPENED_MARK
            case _:
                continue

        # クリア判定
        remaining = 0
        for row in display_stage:
            remaining += row.count(UNOPENED_MARK)
            remaining += row.count(FLAG_MARK)

        if remaining == count_bomb:
            return True, hit_bomb


if __name__ == "__main__":
    # mainの結果（クリア判定と被弾数）を受け取る
    is_clear, final_hit_bomb = main()

    if start_time is None:
        start_time = time.time()

    stop_time = int((time.time() - start_time) * 1000)
    print(f"TIME: {stop_time / 1000:.3f}s")

    if is_clear:
        print("Game Clear!")
        if LEVEL != 4:
            score.save(LEVEL, stop_time)
        else:
            score.save(LEVEL, int(stop_time), final_hit_bomb)

    print("Press Enter key to return to menu...")
    readchar.readkey()
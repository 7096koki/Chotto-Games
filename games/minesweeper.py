import os
import random
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import score, screen, timer, controls

INFO = {
    "title": "minesweeper",
    "rule": "80s kara no teiban PC game. bakudan wo sakete subete no masu wo akeyou!",
    "controls": "↑↓←→: cursor idou | Enter: akeru | space: hata wo tateru | xyz: muteki mode",
    "max_level": 5
}

# 状態を表す定数（マジックワードの共通化）
BOMB_MARK = "*"
UNOPENED_MARK = "□"
FLAG_MARK = "F"

# カーソルの初期位置
y = 0
x = 0

# グローバル変数の定義
SIZE = 9
BOMB = 10
data_stage = []
display_stage = []
count_bomb = 0

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
    global x, y
    global is_cheat
    global SIZE, BOMB, data_stage, display_stage, count_bomb

    level_val = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    match level_val:
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
            BOMB = 10

    # ステージの生成
    data_stage = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    display_stage = [[UNOPENED_MARK for _ in range(SIZE)] for _ in range(SIZE)]

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

    hit_bomb = 0
    remaining = SIZE * SIZE
    input_history = []
    is_cheat = 0

    # 最初のEnterを押す前にタイマーが呼ばれた時用のフラグ管理
    timer_started = False

    while True:
        show_stage()
        print("-" * 40)
        print(INFO["controls"])
        
        # プレイ中も画面に現在のタイムをリアルタイム表示
        if timer_started:
            print(f"TIME: {timer.get_elapsed_seconds_str()}")
        else:
            print("TIME: 0.000s")
            
        if is_cheat == 1:
            print(f"Bombs Hit: {hit_bomb}")
        print("-" * 40)

        if is_cheat == 2 and data_stage[y][x] == BOMB_MARK:
            print("#")

        key = controls.readkey()

        if isinstance(key, str):
            input_history.append(key.lower())
            if len(input_history) > 5:
                input_history.pop(0)

        if "".join(input_history) == "xyz":
            is_cheat = 1

        if "".join(input_history) == "xyzzy":
            is_cheat = 2

        match key:
            case "DOWN":
                y = min(SIZE - 1, y + 1)
            case "UP":
                y = max(0, y - 1)
            case "LEFT":
                x = max(0, x - 1)
            case "RIGHT":
                x = min(SIZE - 1, x + 1)
            case "ENTER":
                # タイマーの起動を共通ライブラリの関数に変更
                if not timer_started:
                    timer.start()
                    timer_started = True

                if display_stage[y][x] != UNOPENED_MARK:
                    continue

                if data_stage[y][x] == BOMB_MARK:
                    level_val = int(sys.argv[1]) if len(sys.argv) > 1 else 1
                    if level_val == 4:
                        hit_bomb += 1
                        display_stage[y][x] = BOMB_MARK
                        continue
                    else:
                        game_over()
                        return False, hit_bomb

                open_cell(y, x)
            case "SPACE":
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
    level_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    is_clear, final_hit_bomb = main()

    stop_time = timer.get_elapsed_ms()
    print(f"FINAL TIME: {timer.get_elapsed_seconds_str()}")

    if is_clear:
        print("Game Clear!")
        match is_cheat:
            case 1:
                score.save("minesweeper", level_arg, stop_time, final_hit_bomb)
            case 2:
                score.save("minesweeper", level_arg, stop_time, "Cheat_mode")
            case _:
                score.save("minesweeper", level_arg, stop_time)

    print("Press Enter key to return to menu...")
    controls.readkey()
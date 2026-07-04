import random
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from lib import screen


def main():
    count = 0
    n = random.randint(1, max_n)

    while True:
        try:
            print(
                "answer: ", end="", flush=True
            )  # inputに書いても何故か表示されないので応急処置
            answer = int(input())
        except ValueError:
            print("This is not number")
            continue

        count += 1

        if answer < n:
            print("It's bigger number(+)")
        elif answer > n:
            print("It's smaller number(-)")
        elif answer == n:
            print(f"Correct answer after {count} time!")
            input("Press any key to return to menu...")
        elif level > 1 and abs(n - answer) < (max_n / 10):
            # 10^(level-1) の数値を計算して表示
            hint_range = 10 ** (level - 1)
            print(f"±{hint_range}")


if __name__ == "__main__":
    level = int(sys.argv[1])
    max_n = 10**level
    print(f"Lv.{level}: 1 ~ {max_n}")
    main()

import random
import os
import sys

def main():
    count = 0
    n = random.randint(1, max_n)

    while True:
        try:
            print("answer: ", end="", flush=True) # inputに書いても何故か表示されないので応急処置
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
        if abs(n - answer) <= 10 and not level == 1:
            print("±10")

    
if __name__ == "__main__":
    level = int(sys.argv[1])
    max_n = 10 ** level
    print(f"Lv.{level}: 1 ~ {max_n}")
    main()
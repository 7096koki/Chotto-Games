import random

def main():
    count = 0
    n = random.randint(1, max_n)

    while True:
        try:
            answer = int(input("answer: "))
        except ValueError:
            print("this is not number")
            continue

        count += 1

        if answer < n:
            print("+")
        elif answer > n:
            print("-")
        elif answer == n:
            print(f"Correct answer after {count} time!")
            break
        if abs(n - answer) <= 10 and not level == 1:
            print("±10")

    
if __name__ == "__main__":
    level = 1
    while True:
        max_n = 10 ** level
        print(f"Lv.{level}: 1 ~ {max_n}")
        main()
        level += 1
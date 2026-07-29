def clear(row=2):
    print(f"\x1b[{row};1H\x1b[J", end="")

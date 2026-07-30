import sys

# OS判定してモジュールを切り替え
if sys.platform == "win32":
    import msvcrt

    def readkey():
        """Windows環境での1キー取得"""
        ch = msvcrt.getch()

        # 矢印キーなどの特殊キー（2バイト送られてくる）のハンドリング
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            match ch2:
                case b"H":
                    return "UP"
                case b"P":
                    return "DOWN"
                case b"M":
                    return "RIGHT"
                case b"K":
                    return "LEFT"
                case _:
                    return ""

        # 通常のキー（エンター、スペース、文字など）
        match ch:
            case b"\r" | b"\n":
                return "ENTER"
            case b" ":
                return "SPACE"
            case _:
                try:
                    return ch.decode("utf-8")
                except UnicodeDecodeError:
                    return ""

else:
    import sys
    import termios
    import tty

    def readkey():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)

            # 矢印キー（エスケープシーケンス: \x1b[A など）の判定
            if ch == "\x1b":
                # 後続の2文字を読み込む
                seq = sys.stdin.read(2)
                match seq:
                    case "[A":
                        return "UP"
                    case "[B":
                        return "DOWN"
                    case "[C":
                        return "RIGHT"
                    case "[D":
                        return "LEFT"
                    case _:
                        return "ESC"

            # 通常のキー判定
            match ch:
                case "\r" | "\n":
                    return "ENTER"
                case " ":
                    return "SPACE"
                case _:
                    return ch

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
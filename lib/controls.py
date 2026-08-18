import sys

IS_POSIX = sys.platform.startswith(("linux", "darwin", "freebsd", "openbsd", "android"))
IS_WIN = sys.platform in ("win32", "cygwin")

if IS_POSIX:
    import termios
    import tty

    def _getch() -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # 端末をrawモードに変更（1文字ずつ即時読み込み）
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            # 属性を必ず元に戻す
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

elif IS_WIN:
    import msvcrt

    def _getch() -> str:
        return msvcrt.getwch()

else:
    raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def readkey() -> str:
    """キー入力を1回分取得し、扱いやすい文字列で返します。"""
    ch = _getch()

    # Ctrl+C (Interrupt)
    if ch == "\x03":
        raise KeyboardInterrupt

    if IS_POSIX:
        # Enter (Mac/Linuxでは \r や \n が来ます)
        if ch in ("\r", "\n"):
            return "ENTER"
        if ch == " ":
            return "SPACE"
        if ch in ("\x7f", "\x08"):
            return "BACKSPACE"

        # エスケープシーケンス（矢印キーなど）
        if ch == "\x1b":
            # 次の文字があるか確認
            c2 = _getch()
            if c2 == "[":
                c3 = _getch()
                if c3 == "A":
                    return "UP"
                elif c3 == "B":
                    return "DOWN"
                elif c3 == "C":
                    return "RIGHT"
                elif c3 == "D":
                    return "LEFT"
                elif c3 == "Z":
                    return "SHIFT_TAB"
                return "\x1b[" + c3
            return "\x1b" + c2

        return ch

    elif IS_WIN:
        # Enter / Space / Backspace
        if ch in ("\r", "\n"):
            return "ENTER"
        if ch == " ":
            return "SPACE"
        if ch == "\x08":
            return "BACKSPACE"

        # 特殊キー（矢印キーなど）
        if ch in ("\x00", "\xe0"):
            code = _getch()
            if code == "H":
                return "UP"
            elif code == "P":
                return "DOWN"
            elif code == "K":
                return "LEFT"
            elif code == "M":
                return "RIGHT"
            return "\x00" + code

        return ch

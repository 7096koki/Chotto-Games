import time
from decimal import Decimal, ROUND_HALF_UP

_start_time = None

def start():
    """タイマーを開始する"""
    global _start_time
    _start_time = time.time()

def get_elapsed_ms():
    """開始からの経過時間をミリ秒(int)で取得する"""
    if _start_time is None:
        return 0
    return int((time.time() - _start_time) * 1000)

def get_elapsed_seconds_str():
    """正確な文字列を取得する"""
    ms = get_elapsed_ms()
    # decimalを使って正確に小数点以下3桁で四捨五入する
    seconds = Decimal(str(ms)) / Decimal("1000")
    return str(seconds.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)) + "s"
def parity(x: int) -> int:
    par = 0
    while x != 0 and x != -1:
        par ^= x & 1
        x = int(x / 2)
    return par


class Colors:
    SVG_BLACK = "#000000"
    SVG_WHITE = "#FFFFFF"
    SVG_RED = "#FF0000"
    PYG_WHITE = (255, 255, 255)

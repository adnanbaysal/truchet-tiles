def parity(x: int) -> int:
    par = 0
    while x != 0 and x != -1:
        par ^= x & 1
        x = int(x / 2)
    return par

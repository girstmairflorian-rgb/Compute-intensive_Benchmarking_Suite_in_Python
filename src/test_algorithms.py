import math

def check_if_prime(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True

def fibonacci(n: int) -> int:
    a, b = 0, 1

    if n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(1, n):
            c = a + b
            a, b = b, c
        return b
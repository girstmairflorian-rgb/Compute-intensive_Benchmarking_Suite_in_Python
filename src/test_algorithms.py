import math

def check_if_prime(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True

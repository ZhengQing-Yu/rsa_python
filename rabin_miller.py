from math import gcd
import random

base = (2, 3, 5, 7, 11, 13, 17)


def is_prime(n):
    def rabin_miller_test(a, n):
        if a == n:
            return True
        if gcd(a, n) != 1:
            return False
        x = pow(a, m, n)
        if x == 1 or x == n - 1:
            return True
        for i in range(s - 1):
            x = (x ** 2) % n
            if x == n - 1:
                return True
            if x == 1:
                return False
        return False

    r = (n-1)//2
    m = 0
    s = 0
    for i in range(n):
        if r % 2 == 1:
            m = int(r)
            s = i+1
            break
        else:
            r = r//2

    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for a in base:
        if not(rabin_miller_test(a, n)):
            return False
    return True


def generate_random(stop=4000000000, start=0):
    n = random.randint(start, stop)
    while not is_prime(n):
        n = random.randint(start, stop)
    return n

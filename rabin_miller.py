import math
import random
from mod_operation import mod_power

# works up to 2^56

base = (2, 3, 5, 7, 11, 13, 17)


# Euclid's algorithm for GCD
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def prime(n):
    def rabin_miller_test(a, n):
        if a == n:
            return True
        if gcd(a, n) != 1:
            return False
        x = mod_power(a, m, n)
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


def is_Prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


for i in range(1000000000000000000000000000, 1000000000000000000000000999):
    if prime(i) != is_Prime(i):
        print(i)

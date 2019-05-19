# computes a^n mod m using the divide and multiply algorithm
def mod_power(a, n, m):
    n_binary = "{0:b}".format(n)
    x = 1
    exp_counter = a % m
    for i in range(len(n_binary)):
        if int(n_binary[-i-1]) == 1:
            x = (x * exp_counter) % m
        exp_counter = (exp_counter ** 2) % m
    return x


# computes a^-1 mod n
def mod_inverse(a, n):
    quotients = []
    remainder = a
    divisor = a
    dividend = n
    while remainder != 0:
        quotients.append(dividend//divisor)
        remainder = dividend % divisor
        dividend = divisor
        divisor = remainder
    quotients.pop()
    back_substitution1 = 1
    back_substitution2 = -quotients.pop()
    placeholder = 1
    while quotients:
        back_substitution1 = back_substitution2
        back_substitution2 = placeholder - quotients.pop()*back_substitution2
        placeholder = back_substitution1
    return back_substitution2 % n


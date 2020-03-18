# computes base^exponent mod modulo using the divide and multiply algorithm
def mod_power(base, exponent, modulo):
    x = 1
    current_power = base % modulo
    while exponent != 0:
        remainder = exponent % 2
        exponent = exponent // 2
        if remainder == 1:
            x = (x * current_power) % modulo
        current_power = (current_power ** 2) % modulo
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


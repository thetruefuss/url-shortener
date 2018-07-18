import string

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(CHARS)


def decimal_to_base_n(number):
    if number >= BASE:
        return decimal_to_base_n(number // BASE) + CHARS[number % BASE]
    else:
        return CHARS[number]


def base_n_to_decimal(number):
    if len(number) > 1:
        return base_n_to_decimal(number[:-1]) * BASE + CHARS.index(number[-1])
    else:
        return CHARS.index(number[0])

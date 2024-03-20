import random

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as (2^r)*d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        # Generate a random number of specified bit length
        candidate = random.getrandbits(bits)

        # Ensure the number has the correct bit length
        candidate |= (1 << bits - 1) | 1

        if is_prime(candidate):
            return candidate

def generate_generator(p):
    # For a prime p, generator g must be in the range [2, p-2]
    for g in range(2, p - 1):
        if pow(g, (p - 1) // 2, p) != 1 and pow(g, p - 1, p) == 1:
            return g

def generate_p_g(bits):
    # Generate p and g
    p = generate_prime(bits)
    g = generate_generator(p)
    return p,g
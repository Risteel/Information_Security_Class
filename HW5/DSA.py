import pickle
import secrets
import sys
from hashlib import sha1

class struct:
    def __init__(self, **kwarg):
        self.__dict__.update(kwarg)

def randint(a, b):
    ''' Return a random int in the range [a, b).'''
    # random.randrange(a, b) => [a, b)
    # secrets.randbelow(n) => [0, n)
    return secrets.randbelow(b - a) + a

def mul_inv(a, b):
    old_x, x = 1, 0
    old_y, y = 0, 1
    old_r, r = a, b
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_t, y = y, old_y - q * y
    if old_x < 0:
        old_x = old_x + b
    return old_r == 1, old_x

def powmod(a, b, c):
    v = 1
    while b > 0:
        if b & 1 == 1:
            v = (v * a) % c
        a = (a * a) % c
        b = b >> 1
    return v

def MillerRabinTest(N):
    if N < 2:
        return False
    if N == 2 or N == 3:
        return True
    if N & 1 == 1:
        r = N - 1
        m = -r & r
        k = 0
        while m > 1:
            k = k + 1
            m = m >> 1
        m = r >> k
        for _ in range(5):
            a = randint(2, N - 1)
            b = powmod(a, m, N)
            if b != 1 and b != (N - 1):
                i = 1
                while i < k and b != (N - 1):
                    b = (b * b) % N
                    if b == 1:
                        return False
                    i = i + 1
                if b != (N - 1):
                    return False
        return True
    else:
        return False

def _ceil(a, b):
    x = divmod(a, b)
    return x[0] + (x[1] > 0)

def generate_keys(bits):
    p_max = (1 << 1024) - 1
    p_min = 1 << (1024 - 1)
    flag1 = True
    while flag1:
        flag2 = True
        max_count = 50
        q = secrets.randbits(bits) | (1 << bits - 1) | 1
        k_min = _ceil(p_min, q)
        k_max = (p_max // q) + 1
        while flag2:
            k = randint(k_min, k_max)
            p = k * q + 1
            if MillerRabinTest(p):
                flag1 = flag2 = False
            elif max_count <= 0:
                flag2 = False
            max_count -= 1
    a = powmod(randint(1, p - 1), k, p)
    d = randint(1, q)
    b = powmod(a, d, p)
    return struct(p=p,q=q,a=a,b=b,d=d)

def sign(x, keys):
    '''
    x: string
    keys: struct, has p , q, a, d
    output: r, s
    '''
    p = keys.p
    q = keys.q
    a = keys.a
    d = keys.d
    succ = False
    m = 1000
    while not succ:
        if m <= 0:
            raise Exception('1000 times faild')
        m -= 1
        ke = randint(1, q)
        succ, ke_inv = mul_inv(ke, q)
        #print("check ke_inv", succ, ke, ke_inv, m)
        if succ:
            r = powmod(a, ke, p) % q
            h = int.from_bytes(sha1(x.encode('utf-8')).digest(), 'big')
            s = ((h + d * r) * ke_inv) % q
            #print("check s_inv", succ, ke, ke_inv, m)
            succ, s_inv = mul_inv(s, q)
    return r, s

def valid(x, r, s, keys):
    '''
    x: string
    r: int
    s: int
    keys: struct, has p, q, a, b
    '''
    p = keys.p
    q = keys.q
    a = keys.a
    b = keys.b
    h = int.from_bytes(sha1(x.encode('utf-8')).digest(), 'big')
    _, w = mul_inv(s, q)
    u1 = (w * h) % q
    u2 = (w * r) % q
    v = (powmod(a, u1, p) * powmod(b, u2, p)) % p % q
    return v == r
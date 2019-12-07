from base64 import b64encode as btoa
from base64 import b64decode as atob
import pickle
import secrets
import sys

def randint(a, b):
    ''' Return a random int in the range [a, b).'''
    # random.randrange(a, b) => [a, b)
    # secrets.randbelow(n) => [0, n)
    return secrets.randbelow(b - a) + a

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

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
    return old_x

def powmod(a, b, c):
    v = 1
    while b > 0:
        if b & 1 == 1:
            v = (v * a) % c
        a = (a * a) % c
        b = b >> 1
    return v

def CRT(x, d, p, q):
    a0 = powmod(x, d % (p - 1), p)
    a1 = powmod(x, d % (q - 1), q)
    u = ((a1 - a0) * mul_inv(p, q)) % q
    return a0 + p * u

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

def generate_prime(b):
    t = secrets.randbits(b)
    while not MillerRabinTest(t):
        t = secrets.randbits(b)
    return t

def generate_p_q_n(b):
    p = q = generate_prime(b >> 1)
    while p == q:
        q = generate_prime(b >> 1)
    return p, q, p * q

def generate_e_d(p, q):
    x = (p - 1) * (q - 1)
    e = x
    while gcd(e, x) != 1:
        e = randint(1, x)
    d = mul_inv(e, x)
    return e, d

def pad(m, bits):
    bits = (bits - 1) >> 3
    PL = bits - (len(m) + 1) % bits
    PS = b''.join([randint(1, 256).to_bytes(1, 'little') for x in range(PL)])
    return PS + b'\0' + m

def unpad(m):
    for i in range(len(m)):
        if m[i] == 0:
            return m[i+1:]
    return b''

class RSA:
    def __init__(self, bits):
        self.p, self.q, self.n = generate_p_q_n(bits)
        self.e, self.d = generate_e_d(self.p, self.q)
        self.n = self.p * self.q
        self.bits = bits
    
    def exportKey(self, fileName='RSA.key'):
        with open(fileName, 'wb') as file:
            pickle.dump(self.__dict__, file)

    def importKey(self, fileName='RSA.key'):
        with open(fileName, 'rb') as file:
            self.__dict__.update(pickle.load(file))
    
    def encrypt(self, plain):
        msg = plain.encode('utf-8')
        msg = pad(msg, self.bits)
        new_msg = b''
        step = (self.bits - 1) >> 3
        size = self.bits >> 3
        for i in range(0, len(msg), step):
            m = msg[i:i + step]
            m = int.from_bytes(m, 'big')
            m = powmod(m, self.e, self.n)
            m = m.to_bytes(size, 'big')
            new_msg = new_msg + m
        return btoa(new_msg).decode('utf-8')
    
    def decrypt(self, cipher):
        msg = cipher.encode('utf-8')
        msg = atob(msg)
        new_msg = b''
        step = (self.bits - 1) >> 3
        size = self.bits >> 3
        for i in range(0, len(msg), size):
            m = msg[i:i + size]
            m = int.from_bytes(m, 'big')
            m = CRT(m, self.d, self.p, self.q) % self.n
            m = m.to_bytes(step, 'big')
            new_msg = new_msg + m
        new_msg = unpad(new_msg)
        return new_msg.decode('utf-8')

def main():
    if len(sys.argv) > 1:
        opt = sys.argv[1]
        a = RSA(1024)
        if opt == 'init':
            bits = int(sys.argv[2])
            a = RSA(bits)
            if len(sys.argv) >= 4:
                a.exportKey(sys.argv[3])
            else:
                a.exportKey()
        elif opt == 'encrypt':
            mode = sys.argv[2]
            if mode == 'file':
                with open(sys.argv[3], encoding='utf-8') as file:
                    plain = file.read()
            elif mode == 'text':
                plain = sys.argv[3]
            else:
                print('not support option: %s' % mode)
                return
            if len(sys.argv) >= 5:
                a.importKey(sys.argv[4])
            else:
                a.importKey()
            ciphertext = a.encrypt(plain)
            with open('Cipertext.txt', 'w') as f:
                f.write(ciphertext)
            print('ciphertext: ', ciphertext)
            print('state: ', a.__dict__)
        elif opt == 'decrypt':
            mode = sys.argv[2]
            if mode == 'file':
                with open(sys.argv[3], encoding='utf-8') as file:
                    ciper = file.read()
            elif mode == 'text':
                ciper = sys.argv[3]
            else:
                print('not support option: %s' % mode)
                return
            if len(sys.argv) >= 5:
                a.importKey(sys.argv[4])
            else:
                a.importKey()
            plaintext = a.decrypt(ciper)
            with open('Plaintext.txt', 'w') as f:
                f.write(plaintext)
            print('plaintext: ', plaintext)
            print('state: ', a.__dict__)
        else:
            print('not support option: %s' % opt)

if __name__ == '__main__':
    main()
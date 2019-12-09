import math
import random
import sys
import base64
import numpy as np


#ax + by = gcd(a,b)    
def ExtendEuclidean(a,b):
    r0,r1 = a , b
    x0,x1 = 1 , 0
    y0,y1 = 0 , 1
    r,x,y = 1,1,1
    while r != 0:
        q = a//b
        r = r0 - q * r1
        x = x0 - q * x1
        y = y0 - q * y1
        r0,r1 = r1,r
        x0,x1 = x1,x
        y0,y1 = y1,y
        a,b = b,r
    return y0

def GeneratePrimeNumber(bits):
    base = (1 << (bits - 1) ) | 1
    upperbound = (1 << (bits - 2) ) - 1
    #use Miller Rabin test to find likely prime number
    while True:
        n = random.randint(0, upperbound) << 1
        p = base + n
        if Miller_Rabin(p) is True: break
    while True:
        n = random.randint(0, upperbound) << 1
        q = base + n
        if Miller_Rabin(q) is True and q != p: break
    return p,q

def GenerateKey(phi):
    #find number e, gcd(e,phi) is 1
    while True:
        e = random.randint(2,phi - 1)
        if math.gcd(e,phi) == 1: break
    #use extended euclidean find inveres e on mod phi
    d = ExtendEuclidean(phi,e)
    d = d % phi
    return e,d

def pad(text,bits = 1024):
    padding = bits - ((len(text) + 1) % bits)
    return text + b'\0' + np.random.bytes(padding)

def unpad(text):
    bits = len(text)
    for i in range(bits):
        if text[i] == 0:
            return text[0:i]

def pow_mod(x, y, z):
    #Calculate (x ** y) % z efficiently.
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

def selectBase(choose,N):
    select = True
    #select base in range 2 to N-2
    while select == True:
        a = random.randint(2 , N - 2)
        select = False
        #if base exist in array of choose,base select again
        for num in choose:
            if a == num: 
                select = True
                break 
    choose.append(a)
    return a , choose
        
#find likely prime number        
def Miller_Rabin(N):
    m = N - 1
    k = 0
    choose = []
    #find N - 1 = 2^k * m
    while m % 2 == 0: 
        k += 1
        m  = m >> 1
    # Use Miller Rabin test five times
    for i in range(5):
        a , choose = selectBase(choose,N)
        b = pow_mod(a,m,N)
        if b != 1 and b != (N-1):
            i = 1
            while i < k and b != (N-1):
                b = pow_mod(b,2,N)
                if b == 1: return False
                i = i + 1
            if b != (N-1):
                return False
    return True


def CountBits(N):
    temp = N
    bits = 0
    while temp > 0:
        bits += 1
        temp = temp >> 1
    return bits


def Encrypt(text,N,e):
    #count bits of N
    bits = CountBits(N)
    #convert to bits of q or p
    bits = (bits // 2) + (bits % 2) 
    #convert plaintext to byte
    plain_byte = pad(text.encode(),bits)
    byteLen = len(plain_byte)
    #count how many byte to encrypt
    byte = bits >> 3
    #count how many bytes of ciphter text
    size = (CountBits(N - 1) >> 3) + 1
    cipher = b''
    for i in range(0,byteLen,byte):
        t = int.from_bytes(plain_byte[i:i + byte],byteorder = 'big')
        t = pow_mod(t,e,N)
        t = t.to_bytes(size,byteorder = 'big')
        cipher += t
    return base64.b64encode(cipher).decode()
    print('Cipher Text: {}'.format(base64.b64encode(cipher).decode()))

def CRT_decrypt(p,q,d,ciphertext):
    dp = d % (p - 1)
    dq = d % (q - 1)
    m1 = pow_mod(ciphertext,dp,p)
    m2 = pow_mod(ciphertext,dq,q)
    p_inverse = ExtendEuclidean(q,p)
    u = (m2 - m1) * p_inverse % q
    return m1 + p * u

def Decrypt(text,N,d, p = 0 , q = 0):
    cipher = base64.b64decode(text.encode())
    byteLen = len(cipher)
    #count how many byte to decrypt
    byte = (CountBits(N - 1) >> 3) + 1
    #count bits of N
    bits = CountBits(N)
    #convert to bits of q or p
    bits = (bits // 2) + (bits % 2)
    #count how many bytes of plain text
    size = (bits >> 3)
    plain = b''
    CRT = bool(p!=0 and q!=0)
    for i in range(0,byteLen,byte):
        t = int.from_bytes(cipher[i:i + byte], byteorder = 'big')
        t = (CRT and CRT_decrypt(p,q,d,t)) or pow_mod(t,d,N)
        t = t.to_bytes(size,byteorder = 'big')
        plain += t
    return unpad(plain).decode()

if __name__ == "__main__":
    try:
        assert(len(sys.argv) >= 2)
        if sys.argv[1] == 'init': #generate p,q,e,d
            if len(sys.argv) != 3 : raise Exception("Init parameter error\nparameter: Init {bits}")
            if sys.argv[2].isnumeric is False: raise Exception("Init bits number are not number")
            bits = int(sys.argv[2])
            if bits < 2: raise Exception("Init bits number are not enough find two prime number")
            p , q = GeneratePrimeNumber(bits)
            N = q * p
            phi = (q-1) * (p-1)
            e , d = GenerateKey(phi)
            print("p: {}\nq: {}\nN: {}\ne: {}\nd: {}".format(p,q,N,e,d))
        elif sys.argv[1] == '-e': 
            if len(sys.argv) != 5 : raise Exception("Encrypt parameter error\nparameter: -e plaintext {N} {e}")
            if sys.argv[3].isnumeric is False or sys.argv[4].isnumeric is False :  raise Exception("Type error,your N or e is not a number")
            cipher = Encrypt(sys.argv[2] , int(sys.argv[3]) , int(sys.argv[4]))
            print('Cipher Text: {}'.format(cipher))
        elif sys.argv[1] == '-d': 
            if len(sys.argv) != 5 and len(sys.argv) != 7: raise Exception("Decrypt parameter error\nparameter: -d plaintext {N} {d} or -d plaintext {N} {d} {p} {q}")
            if sys.argv[3].isnumeric is False or sys.argv[4].isnumeric is False :  raise Exception("Type error,your N or d is not a number")
            if len(sys.argv) == 7:
                plain = Decrypt(sys.argv[2] , int(sys.argv[3]) , int(sys.argv[4]) , int(sys.argv[5]) , int(sys.argv[6]))
            else:
                plain = Decrypt(sys.argv[2] , int(sys.argv[3]) , int(sys.argv[4]))
            print('Plain Text: {}'.format(plain))
        else: raise Exception("Error command\nYou need input RSA.py {init/-e/-d}")
    except Exception as error:
        print(error)
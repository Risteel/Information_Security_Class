from PIL import Image
from Crypto.Cipher import AES
import os

def pad(text):
    padding = 16 - (len(text) % 16)
    return text + bytes([padding] * padding)
    
def unpad(text):
    padding = text[-1]
    for char in text[-padding:]:
        assert char == padding
    return text[:-padding]
def ReadPPM(fileName):
    with open(fileName, "rb") as image:
        f = image.readlines()
    return f

def encrypt(ppmPicture,iv):
    #key2
    key2 = b'0000000000000000'
    #read ppm
    f = ReadPPM(ppmPicture)
    # get image head and body    
    head = b''.join(f[0:3])
    body = bytearray(b''.join(f[3:]))
    #padding body
    body = pad(body)
    tempBody = body
    #calc block size
    blockSize = int(len(body) / 16)
    #encrypt myself block
    iv = bytearray(iv)  
    for i in range(blockSize):
        plaintext = body[i * 16 : (i+1) * 16]
        block = bytearray(a ^ b for (a,b) in zip(plaintext,iv))
        body[i * 16 : (i+1) * 16] = aes.encrypt(block)
        #next iv is encrypt block
        iv = body[i * 16 : (i+1) * 16]
        #block xor key2 after encrypt block
        body[i * 16 : (i+1) * 16] = bytearray(a ^ b for (a,b) in zip(body[i * 16 : (i+1) * 16],key2))
        #next key2 is previous plaintext
        key2 = plaintext
    #merge head and body
    img = head + body
    newFile = open("encrypt.ppm","wb")
    newFile.write(img)

    ppmPicture = ("encrypt.ppm")
    im = Image.open(ppmPicture)
    im.save("encrypt.jpg")

def decrypt(ppmPicture,iv):
    #key2
    key2 = b'0000000000000000'
    #read ppm
    f = ReadPPM(ppmPicture)   
    # get image head and body       
    head = b''.join(f[0:3])
    body = bytearray(b''.join(f[3:]))
    #calc block size
    blockSize = int(len(body) / 16)
    #decrypt myself block
    iv = bytearray(iv)
    for i in range(blockSize):
        ciphertext = body[i * 16 : (i+1) * 16]
        block = bytearray(a ^ b for (a,b) in zip(ciphertext,key2))
        body[i * 16 : (i+1) * 16] = aes.decrypt(block)
        body[i * 16 : (i+1) * 16] = bytearray(a ^ b for (a,b) in zip(body[i * 16 : (i+1) * 16],iv))
        key2 = body[i * 16 : (i+1) * 16]
        iv = block


    img = head + body
    newFile = open("decrypt.ppm","wb")
    newFile.write(img)
    body = unpad(body)
    img = head + body
    ppmPicture = ("decrypt.ppm")
    im = Image.open(ppmPicture)
    im.save("decrypt.jpg")

if __name__ == '__main__':
    iv = input("> please input iv: ").encode()
    key = input("> please input key: ").encode()
    print("please select mode,encrypt is 0,decrypt is 1")
    mode = int(input("> please input mode: "))
    try:
        if len(iv) != 16 or len(key) != 16:
            raise Exception("key or iv length error")
        if mode != 0 and mode != 1:
            raise Exception("mode error")

        aes = AES.new(key, AES.MODE_ECB)
        if mode == 0:
            im = Image.open('tux.jpg')
            ppmPicture = ("origin.ppm")
            im.save(ppmPicture)
            encrypt(ppmPicture,iv)
        else:
            ppmPicture = ("encrypt.ppm")
            decrypt(ppmPicture,iv)
    except Exception as error:
        print(error)




   





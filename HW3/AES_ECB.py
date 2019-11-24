import sys
from PIL import Image
from Crypto.Cipher import AES
import os

def pad(d):
	padding = 16 - (len(d) % 16)
	return d + bytes([padding] * padding)

def unpad(d):
	padding = d[-1]
	return d[:-padding]

def HAB(filename):
    '''get ppm file header and body'''
    with open(filename, 'rb') as ppm:
        lines = ppm.readlines()
        return b''.join(lines[:3]), b''.join(lines[3:])

def main(input_file, output_file):
    ppm_name = os.path.splitext(sys.argv[1])[0]

    # Create a ppm file
    with Image.open(input_file) as img:
        img.save(ppm_name + "_origin.ppm")

    # Initialize an AES cipher in ECB mode
    aes = AES.new(os.urandom(32), AES.MODE_ECB)
    
    # encrypt
    head, body = HAB(ppm_name + "_origin.ppm")
    body = pad(body)
    new_body = b''
    for i in range(0, len(body), 16):
        block = body[i:i+16]
        new_body += aes.encrypt(block)
    new_ppm = head + new_body
    
    # Save encrypted ppm file
    with open(ppm_name + "_encrypt.ppm", 'wb') as new_file:
        new_file.write(new_ppm)
    
    # Save as a file in another format
    with Image.open(ppm_name + "_encrypt.ppm") as img:
        img.save(output_file)
    
    # decrypt
    head, body = HAB(ppm_name + "_encrypt.ppm")
    new_body = b''
    for i in range(0, len(body), 16):
        block = body[i:i+16]
        new_body += aes.decrypt(block)
    new_body = unpad(new_body)
    new_ppm = head + new_body
    
    # Save decrypted ppm file
    with open(ppm_name + "_decrypt.ppm", 'wb') as new_file:
        new_file.write(new_ppm)
    
    # convert ppm to png
    with Image.open(ppm_name + "_decrypt.ppm") as img:
        img.save(ppm_name + "_decrypt.png")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("python AES_ECB.py Tux.jpg Tux.png")
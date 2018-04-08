from PIL import Image
import numpy
from django.shortcuts import redirect
import multiprocessing

FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

#KEY = '0111111101'
KEY = '0110100101'


def permutate(original, fixed_key):
    new = ''
    for i in fixed_key:
        new += original[i - 1]
    return new


def left_half(bits):
    return bits[:int(len(bits)/2)]


def right_half(bits):
    return bits[int(len(bits)/2):]


def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half


def key1():
    return permutate(shift(permutate(KEY, FIXED_P10)), FIXED_P8)


def key2():
    return permutate(shift(shift(shift(permutate(KEY, FIXED_P10)))), FIXED_P8)


def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new


def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, FIXED_EP)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S0) + lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits, FIXED_P4)
    return xor(bits, L)


def encrypt(plain_text):
    bits = permutate(plain_text, FIXED_IP)
    temp = f_k(bits, key1())
    bits = right_half(bits) + temp
    bits = f_k(bits, key2())
    encr=permutate(bits + temp, FIXED_IP_INVERSE)
    #print(encr)
    return encr


def decrypt(cipher_text):
    bits = permutate(cipher_text, FIXED_IP)
    temp = f_k(bits, key2())
    bits = right_half(bits) + temp
    bits = f_k(bits, key1())
    decr=permutate(bits + temp, FIXED_IP_INVERSE)
    #print(decr)
    return decr

def encryp(arr):
    for i,j in enumerate(arr):
     for a,b in enumerate(j):
       binary=bin(b)[2:].zfill(8)
       encr=encrypt(binary)
       print(j[a])
       j[a]=int(encr,2)
    return arr


def decryp(arr):
    for i,j in enumerate(arr):
     for a,b in enumerate(j):
       binary=bin(b)[2:].zfill(8)
       decr=decrypt(binary)
       print(j[a])
       j[a]=int(decr,2)
    return arr

def encryption(img):
 img = Image.open(img)
 print(img)
 arr = numpy.array(img)
 #print(list(arr))

 pool=multiprocessing.Pool(8)
 arr=pool.map(encryp, arr)


 img = Image.fromarray(numpy.array(arr))
 filename='encryptedImg.png'
 img.save('img/'+filename)
 print(filename)
 return filename
 img.show()


def decryption(path):
 img = Image.open(path)
 arr = numpy.array(img,dtype='uint8')
 #print(arr)


 pool=multiprocessing.Pool(8)
 arr=pool.map(decryp, arr)

 img = Image.fromarray(numpy.array(arr))
 filename='decryptedImg.png'
 img.save('img/'+filename)
 return filename
 img.show()



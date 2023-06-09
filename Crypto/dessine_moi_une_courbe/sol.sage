from sage.all import *
from Crypto.Cipher import AES
from binascii import unhexlify
import hashlib

p = 231933770389389338159753408142515592951889415487365399671635245679612352781

# Two points on the curve, from data.txt
x1 = 93808707311515764328749048019429156823177018815962831703088729905542530725
y1 = 144188081159786866301184058966215079553216226588404139826447829786378964579
x2 = 139273587750511132949199077353388298279458715287916158719683257616077625421
y2 = 30737261732951428402751520492138972590770609126561688808936331585804316784

# https://crypto.stackexchange.com/questions/97811/find-elliptic-curve-parameters-a-and-b-given-two-points-on-the-curve
# To be able to find a the only problem is the existence of the modular multiplicative inverse of (x1−x2) mod p.
# a = [(y1^2-y2^2)-(x1^3-x2^3)](x1-x2)^-1 mod p; b = (y1^2-x1^3)-ax1
Zp = IntegerModRing(p)
x = Zp(x1-x2)
y = Zp((y1**2 - y2**2) - (x1**3 - x2**3))
a = Zp(((y1**2 - y2**2) - (x1**3 - x2**3)) * (x**-1))
b = Zp(y1**2 - x1**3 - a*x1)
#print(a, b)

#a = 14902775479549176103916693271068277706052934716440896707334978512750519253
#b = 220048944991955967308525489300590382240260882141745561912602020777012600739

# Cipher and IV, from data.txt
cipher = unhexlify('8233d04a29befd2efb932b4dbac8d41869e13ecba7e5f13d48128ddd74ea0c7085b4ff402326870313e2f1dfbc9de3f96225ffbe58a87e687665b7d45a41ac22')
iv = unhexlify('00b7822a196b00795078b69fcd91280d')

# Decrypt
key = str(a) + str(b)
aes = AES.new(hashlib.sha1(key.encode()).digest()[:16], AES.MODE_CBC, iv=iv)
flag = aes.decrypt(cipher)
print(flag.decode())

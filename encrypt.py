from secret import message
import string
from Crypto.Util.number import *

def rndm_str():
    return string.printable[:94][getRandomRange(0, 93)]
def fnd_plc(char):
    return string.printable[:94].index(char)
def encrypt(msg):
    encrypted = ""
    for i in range(len(msg)):
        encrypted += string.printable[:94][(fnd_plc(msg[i]) + 51) % 94]
        encrypted += rndm_str()
    return encrypted
enc = encrypt(message)
# Write(enc, Readme.md)

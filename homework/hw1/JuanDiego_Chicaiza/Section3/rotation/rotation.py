#rotation problem
import os
from unittest import result

encripted_text = open("encrypted.txt", "r").read()


def rotate(text, n):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
            result += chr((ord(char) + n-65) % 26 + 65)
        elif (char.islower()):
            result += chr((ord(char) + n - 97) % 26 + 97)
        else:
            result += char
    return result

for i in range(26):
    print("Primer metodo")
    print("Rotation " + str(i) + ": " + rotate(encripted_text, i))  
    print("Segundo metodo")
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    print("Rotation " + str(i) + ": " + encripted_text.translate(str.maketrans(
        upper + lower,
        upper[i:] + upper[:i] + lower[i:] + lower[:i]
    )))
    print("\n")
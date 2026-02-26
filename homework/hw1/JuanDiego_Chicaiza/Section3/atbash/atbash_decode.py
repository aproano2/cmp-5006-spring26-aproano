import string

#first: steghide extract -sf atbash.jpg -p "" -xf hidden.txt

with open('hidden.txt', 'r') as f:
    ciphertext = f.read().strip()

# Method 1: Using Mathematical Character Shifting
def decrypt_atbash_method1(text):
    decrypted = ""
    for char in text:
        if char.isupper():
            decrypted += chr(ord('Z') - ord(char) + ord('A'))
        elif char.islower():
            decrypted += chr(ord('z') - ord(char) + ord('a'))
        else:
            decrypted += char
    return decrypted

# Method 2: Using str.maketrans
def decrypt_atbash_method2(text):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    
    # Reverse the alphabets for mapping
    upper_rev = upper[::-1]
    lower_rev = lower[::-1]
    
    # Create translation table
    trans_table = str.maketrans(upper + lower, upper_rev + lower_rev)
    
    return text.translate(trans_table)

print("Method 1 Output:", decrypt_atbash_method1(ciphertext))
print("Method 2 Output:", decrypt_atbash_method2(ciphertext))

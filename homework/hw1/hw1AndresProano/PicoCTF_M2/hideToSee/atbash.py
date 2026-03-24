def atbash(text):
    result = ""
    for c in text:
        if c.isalpha():
            if c.islower():
                result += chr(ord('z') - (ord(c) - ord('a')))
            else:
                result += chr(ord('Z') - (ord(c) - ord('A')))
        else:
            result += c
    return result

cipher = "krxlXGU{zgyzhs_xizxp_7142uwv9}"
print(atbash(cipher))
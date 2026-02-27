import hashlib

target = "f67be16357fb2e251fac856e77ebfd426137768153db97c899a3005806d2eceb"

with open("cheese_list.txt", "r", encoding="utf-8") as f:
    cheeses = [line.strip() for line in f if line.strip()]

for cheese in cheeses:
    lc = cheese.lower().encode()
    for salt in range(256):
        h = hashlib.sha256(lc + bytes([salt])).hexdigest()
        if h == target:
            print("CHEESE:", cheese)
            print("SALT_HEX:", f"{salt:02x}")
            print("SALT_DEC:", salt)
            raise SystemExit
import hashlib

target_hash = "0d0b4e33c20cb9a03c2e115199810388d55da48b03a36f2724a6f44c3cc6641f"

with open("pablo_cheese_list.txt", "r", encoding="utf-8") as f:
    cheeses = [line.strip() for line in f if line.strip()]

tabla = {}

for cheese in cheeses:
    base = cheese.strip().lower().encode("utf-8")
    for salt in range(256):
        h = hashlib.sha256(base + bytes([salt])).hexdigest()
        tabla[h] = (cheese, format(salt, "02x"))

if target_hash in tabla:
    cheese, salt_hex = tabla[target_hash]
    print("ENCONTRADO")
    print("Queso:", cheese)
    print("Salt (hex):", salt_hex)
else:
    print("No encontrado")
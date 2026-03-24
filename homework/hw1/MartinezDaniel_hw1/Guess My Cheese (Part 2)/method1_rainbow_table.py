
import hashlib
import socket
import re

HOST = "verbal-sleep.picoctf.net"
PORT = 65279   # Actualizar con el puerto de la instancia activa en picoCTF

import os
CHEESE_FILE = os.path.join(os.path.dirname(__file__), "cheese_list.txt")

def build_rainbow_table(cheeses):
    table = {}
    for cheese in cheeses:
        for salt_int in range(256):
            data = cheese.lower().encode() + bytes([salt_int])
            digest = hashlib.sha256(data).hexdigest()
            table[digest] = (cheese, format(salt_int, "02x"))
    return table

def recv_all(sock, timeout=5):
    sock.settimeout(timeout)
    buf = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
    except:
        pass
    return buf.decode()

def main():
    with open(CHEESE_FILE) as f:
        cheeses = [line.strip() for line in f if line.strip()]

    print(f"[*] Construyendo rainbow table: {len(cheeses)} quesos x 256 salts...")
    rainbow = build_rainbow_table(cheeses)
    print(f"[*] Rainbow table lista: {len(rainbow)} entradas\n")

    print(f"[*] Conectando a {HOST}:{PORT}...")
    with socket.create_connection((HOST, PORT)) as sock:

        text = recv_all(sock)
        print(text)

        match = re.search(r'[0-9a-fA-F]{64}', text)
        if not match:
            print("[-] No se encontró ningún hash en la respuesta")
            return

        target_hash = match.group().lower()
        print(f"[*] Hash recibido: {target_hash}")

        if target_hash not in rainbow:
            print("[-] Hash no encontrado en la rainbow table")
            return

        cheese, salt = rainbow[target_hash]
        print(f"[*] Queso: {cheese} | Salt: {salt}")

        # Enviar 'g' para iniciar el guess
        sock.sendall(b"g\n")
        text = recv_all(sock, timeout=3)
        print(text)

        # Enviar el nombre del queso
        sock.sendall((cheese + "\n").encode())
        text = recv_all(sock, timeout=3)
        print(text)

        # Enviar el salt (2 hex chars)
        sock.sendall((salt + "\n").encode())
        text = recv_all(sock, timeout=3)
        print(text)

        if "picoCTF{" in text:
            flag = re.search(r'picoCTF\{[^}]+\}', text)
            print(f"\n[FLAG] {flag.group()}")

if __name__ == "__main__":
    main()

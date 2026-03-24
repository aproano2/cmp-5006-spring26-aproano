
"""
Guess My Cheese (Part 2) - Método 2: Brute Force en línea
Sin precomputación. Para cada hash recibido, prueba las 599 x 256
combinaciones en el momento hasta encontrar la coincidencia.
"""

import hashlib
import socket
import re

HOST = "verbal-sleep.picoctf.net"
PORT = 64953  

import os
CHEESE_FILE = os.path.join(os.path.dirname(__file__), "cheese_list.txt")

def crack_hash(target_hash, cheeses):
    """
    Prueba SHA-256(cheese.lower() + salt_byte) para cada queso y salt.
    Retorna (nombre_queso, salt_hex) al encontrar coincidencia.
    """
    for cheese in cheeses:
        for salt_int in range(256):
            data = cheese.lower().encode() + bytes([salt_int])
            if hashlib.sha256(data).hexdigest() == target_hash:
                return cheese, format(salt_int, "02x")
    return None, None

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

    print(f"Lista cargada: {len(cheeses)} quesos")
    print(f"Conectando a {HOST}:{PORT}...")

    with socket.create_connection((HOST, PORT)) as sock:

        text = recv_all(sock)
        print(text)

        match = re.search(r'[0-9a-fA-F]{64}', text)
        if not match:
            print("No se encontró ningún hash en la respuesta")
            return

        target_hash = match.group().lower()
        print(f"Hash recibido: {target_hash}")
        print(f"Iniciando brute force ({len(cheeses) * 256} combinaciones)...")

        cheese, salt = crack_hash(target_hash, cheeses)

        if not cheese:
            print("No se encontró el queso")
            return

        print(f"Queso: {cheese} | Salt: {salt}")

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

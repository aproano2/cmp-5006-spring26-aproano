import hashlib
import os

def crack_cheese_hash(file_path, target_hash):
    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo '{file_path}'")
        return

    print(f"Buscando el queso que coincide con: {target_hash[:10]}...")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Limpiamos espacios y probamos en minúsculas (formato estándar de retos)
            queso_original = line.strip()
            queso_clean = queso_original.lower()
            
            if not queso_clean:
                continue

            # Probamos los 256 posibles valores de 1 byte (2 nibbles)
            for i in range(256):
                salt_byte = bytes([i])
                
                # Intentamos agregando la sal al final (Suffix)
                candidato = queso_clean.encode('utf-8') + salt_byte
                hash_resultado = hashlib.sha256(candidato).hexdigest()

                if hash_resultado == target_hash:
                    print("\n" + "="*30)
                    print("Queso encontrado")
                    print(f"Nombre: {queso_original}")
                    print(f"Sal: {salt_byte.hex()}")
                    print(f"Combinación final: {queso_clean} + byte(0x{salt_byte.hex()})")
                    print("="*30)
                    return

    print("\nNo se encontró ninguna coincidencia en la lista.")

# --- CONFIGURACIÓN ---
TARGET = "e4f87db650036276b732987fe7cb95f3c4bad824ef5d5238bed25c925f595688"
ARCHIVO = "cheese_list.txt"

crack_cheese_hash(ARCHIVO, TARGET)

"""
Buscando el queso que coincide con: e4f87db650...

==============================
Queso encontrado
Nombre: Mascarpone
Sal: 1f
Combinación final: mascarpone + byte(0x1f)
==============================
"""
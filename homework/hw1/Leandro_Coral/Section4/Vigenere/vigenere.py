def vigenere_decrypt(cipher_text, key):
    """
    Descifra un texto usando el cifrado Vigenere.
    Solo descifra letras (A-Z), mantiene números y símbolos sin cambios.
    """
    key = key.upper()
    decrypted = ""
    key_index = 0
    
    for char in cipher_text:
        if char.isalpha():
            # Determinar si es mayúscula o minúscula
            is_upper = char.isupper()
            char = char.upper()
            
            # Obtener el desplazamiento de la clave
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            
            # Descifrar: (C - K) mod 26
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            
            # Mantener el caso original
            if not is_upper:
                decrypted_char = decrypted_char.lower()
            
            decrypted += decrypted_char
            key_index += 1
        else:
            # Mantener números, símbolos y espacios sin cambios
            decrypted += char
    
    return decrypted


def main():
    """
    Función principal - descifrador Vigenere
    """
    # Datos del problema
    cipher_text = "rgnoDVD{O0NU_WQ3_G1G3O3T3_A1AH3S_f85729e7}"
    key = "CYLAB"
    
    print("=" * 70)
    print(" " * 20 + "DESCIFRADOR VIGENERE (Con repeticion de clave)")
    print("=" * 70)
    print()
    print(f"Texto cifrado: {cipher_text}")
    print(f"Clave:         {key}")
    print()
    
    # Descifrar
    decrypted_text = vigenere_decrypt(cipher_text, key)
    
    # Mostrar resultado

    print(f"Texto descifrado: {decrypted_text}")



if __name__ == "__main__":
    main()

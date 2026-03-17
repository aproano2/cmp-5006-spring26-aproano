def rotate_letter(letter, shift):
    """
    Rota una letra por un número específico de posiciones.
    Mantiene mayúsculas y minúsculas.
    """
    if letter.isupper():
        # Para letras mayúsculas (A-Z)
        return chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
    elif letter.islower():
        # Para letras minúsculas (a-z)
        return chr((ord(letter) - ord('a') + shift) % 26 + ord('a'))
    else:
        # No es una letra, se mantiene igual
        return letter


def decrypt_rotation(encrypted_text, shift):
    """
    Desencripta un texto usando rotación (cifrado César).
    Para desencriptar, usamos la rotación negativa.
    """
    decrypted = ""
    for char in encrypted_text:
        decrypted += rotate_letter(char, -shift)
    return decrypted


def try_all_rotations(encrypted_text):
    """
    Prueba todas las posibles rotaciones (0-25) y muestra los resultados.
    """
    print(f"Texto encriptado: {encrypted_text}\n")
    print("=" * 60)
    print("Probando todas las rotaciones posibles:")
    print("=" * 60)
    
    for shift in range(26):
        decrypted = decrypt_rotation(encrypted_text, shift)
        print(f"Rotación {shift:2d}: {decrypted}")
    print("=" * 60)


def decrypt_with_known_shift(encrypted_text, shift):
    """
    Desencripta un texto cuando se conoce el valor de la rotación.
    """
    decrypted = decrypt_rotation(encrypted_text, shift)
    print(f"Texto encriptado: {encrypted_text}")
    print(f"Rotación usada: {shift}")
    print(f"Texto desencriptado: {decrypted}")
    return decrypted


def main():
    """
    Función principal - menú interactivo.
    """
    print("=" * 60)
    print("DESENCRIPTADOR DE ROTACIÓN (CIFRADO CÉSAR)")
    print("=" * 60)
    print()
    
    # Solicitar el texto encriptado
    encrypted_text = input("Ingrese el texto encriptado: ")
    print()
    
    # Opciones
    print("Opciones:")
    print("1. Probar todas las rotaciones posibles (0-25)")
    print("2. Desencriptar con una rotación conocida")
    print()
    
    option = input("Seleccione una opción (1 o 2): ")
    print()
    
    if option == "1":
        try_all_rotations(encrypted_text)
    elif option == "2":
        try:
            shift = int(input("Ingrese el valor de rotación (0-25): "))
            if 0 <= shift <= 25:
                print()
                decrypt_with_known_shift(encrypted_text, shift)
            else:
                print("Error: La rotación debe estar entre 0 y 25.")
        except ValueError:
            print("Error: Ingrese un número válido.")
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()

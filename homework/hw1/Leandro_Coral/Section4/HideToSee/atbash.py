def atbash_decode(text):
    """
    Decodifica (o codifica) texto usando el cifrado Atbash.
    En Atbash: A↔Z, B↔Y, C↔X, D↔W, etc.
    """
    result = ""
    
    for char in text:
        if char.isupper():
            # Para mayúsculas: A=0, Z=25
            # Invertir: A→Z (0→25), B→Y (1→24), etc.
            result += chr(ord('Z') - (ord(char) - ord('A')))
        elif char.islower():
            # Para minúsculas: a=0, z=25
            result += chr(ord('z') - (ord(char) - ord('a')))
        else:
            # Mantener números, espacios y símbolos sin cambios
            result += char
    
    return result


def main():
    """
    Función principal - decodificador interactivo
    """
    print("=" * 60)
    print(" " * 15 + "DECODIFICADOR ATBASH")
    print("=" * 60)
    print()
    print("El cifrado Atbash invierte el alfabeto:")
    print("A↔Z, B↔Y, C↔X, D↔W, E↔V, etc.")
    print()
    print("=" * 60)
    print()
    
    # Solicitar texto a decodificar
    texto_cifrado = input("Ingrese el texto a decodificar: ")
    
    # Decodificar
    texto_decodificado = atbash_decode(texto_cifrado)
    
    # Mostrar resultados
    print()
    print("=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print(f"Texto original:     {texto_cifrado}")
    print(f"Texto decodificado: {texto_decodificado}")
    print("=" * 60)


if __name__ == "__main__":
    main()

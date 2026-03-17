def decode_substitution(cipher_text, mapping):
    """
    Decodifica texto usando un mapeo de sustitución
    """
    result = ""
    for char in cipher_text:
        if char.lower() in mapping:
            if char.isupper():
                result += mapping[char.lower()].upper()
            else:
                result += mapping[char.lower()]
        else:
            result += char
    return result


def analyze_frequency(text):
    """
    Analiza la frecuencia de letras en el texto
    """
    freq = {}
    total = 0
    for char in text.lower():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
            total += 1
    
    # Ordenar por frecuencia
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq, total


def main():
    # Texto cifrado
    cipher_text = "isnfnnpctitnznfmxhisnfwnxxntimjxnctsnascdstushhxuhgqbinftnubfciruhgqnicichktckuxbackdurjnfqmifchimkabturjnfusmxxnkdnisntnuhgqnicichktehubtqfcgmfcxrhktrtingtmagckctifmichkebkamgnkimxtwscusmfnznfrbtnebxmkagmfonimjxntocxxtshwnznfwnjnxcnznisnqfhqnfqbfqhtnhemscdstushhxuhgqbinftnubfciruhgqnicichkctkhihkxrihinmuszmxbmjxntocxxtjbimxthihdnitibankitckinfntinackmkanpucinamjhbiuhgqbinftucnkunanenktcznuhgqnicichktmfnheinkxmjhfchbtmeemcftmkauhgnahwkihfbkkckdusnuoxctitmkanpnubickduhkecdtufcqitheenktnhkisnhisnfsmkactsnmzcxrehubtnahknpqxhfmichkmkacgqfhzctmichkmkaheinksmtnxngnkitheqxmrwnjnxcnznmuhgqnicichkihbusckdhkisnheenktcznnxngnkitheuhgqbinftnubfcirctisnfnehfnmjniinfznscuxnehfinusnzmkdnxctgihtibankitckmgnfcumkscdstushhxtebfisnfwnjnxcnznismimkbkanftimkackdheheenktczninuskcvbntctnttnkicmxehfghbkickdmkneenuicznanenktnmkaismiisnihhxtmkauhkecdbfmichkehubtnkuhbkinfnackanenktcznuhgqnicichktahktkhixnmatibankitihokhwisncfnkngrmtneenuicznxrmtinmusckdisngihmuicznxrisckoxconmkmiimuonfqcuhuiectmkheenktcznxrhfcnkinascdstushhxuhgqbinftnubfciruhgqnicichkismitnnotihdnknfminckinfntickuhgqbinftucnkunmghkdscdstushhxnftinmusckdisngnkhbdsmjhbiuhgqbinftnubfcirihqcvbnisncfubfchtcirghiczmickdisngihnpqxhfnhkisncfhwkmkankmjxckdisngihjniinfanenkaisncfgmusckntisnexmdctqcuhUIE{K6F4G_4K41R515_15_73A10B5_702E03EU}"
    
    print("=" * 80)
    print(" " * 25 + "DECODIFICADOR POR SUSTITUCIÓN")
    print("=" * 80)
    print()
    
    # Pista conocida: "picoctf" → "qcuhuie"
    # Esto significa el mapeo inverso:
    known_mapping = {
        'q': 'p',
        'c': 'i',
        'u': 'c',
        'h': 'o',
        'i': 't',
        'e': 'f',
    }
    
    print("Mapeo conocido de la pista 'picoctf' → 'qcuhuie':")
    print("Cifrado → Original")
    for k, v in sorted(known_mapping.items()):
        print(f"  {k} → {v}")
    print()
    
    # Analizar frecuencia
    print("=" * 80)
    print("ANÁLISIS DE FRECUENCIA DEL TEXTO CIFRADO")
    print("=" * 80)
    freq, total = analyze_frequency(cipher_text)
    print("Letras más frecuentes en el texto cifrado:")
    for i, (char, count) in enumerate(freq[:15]):
        percentage = (count / total) * 100
        print(f"{i+1:2}. '{char}': {count:3} veces ({percentage:5.2f}%)")
    print()
    
    # Frecuencias típicas en inglés
    print("Frecuencias típicas en inglés:")
    print("e(12.7%), t(9.1%), a(8.2%), o(7.5%), i(7.0%), n(6.7%), s(6.3%)")
    print()
    
    # Decodificar con el mapeo conocido
    print("=" * 80)
    print("DECODIFICACIÓN PARCIAL (con mapeo conocido)")
    print("=" * 80)
    partial_decode = decode_substitution(cipher_text, known_mapping)
    print(partial_decode[:500])
    print("...")
    print()
    
    # Buscar el flag
    print("=" * 80)
    print("BUSCANDO EL FLAG (picoCTF{...})")
    print("=" * 80)
    flag_start = cipher_text.find("qcuhUIE")
    if flag_start != -1:
        flag_cipher = cipher_text[flag_start:flag_start+50]
        flag_decoded = decode_substitution(flag_cipher, known_mapping)
        print(f"Flag cifrado:  {flag_cipher}")
        print(f"Flag parcial:  {flag_decoded}")
        print()
    
    # Intentar completar el mapeo basándose en palabras comunes
    print("=" * 80)
    print("ANÁLISIS: Buscando patrones para completar el mapeo")
    print("=" * 80)
    
    # Basandonos en el texto parcial, voy a intentar deducir más letras
    # "isn" probablemente es "the" (muy común en inglés)
    # "tsnfn" debería ser "there" si i→t, s→h, n→e
    extended_mapping = known_mapping.copy()
    extended_mapping.update({
        's': 'h',
        'n': 'e',
        'f': 'r',
        'm': 'a',
        'x': 'l',
        'b': 'u',
        'r': 'y',
        't': 's',
        'd': 'g',
        'k': 'n',
        'w': 'w',
        'j': 'b',
        'a': 'd',
        'z': 'v',
        'g': 'm',
        'o': 'k',
        'v': 'q',
        'p': 'x',
        'y': 'j',
    })
    
    print("Mapeo extendido (deducido por análisis):")
    for k, v in sorted(extended_mapping.items()):
        print(f"  {k} → {v}", end="  ")
        if list(sorted(extended_mapping.items())).index((k, v)) % 5 == 4:
            print()
    print("\n")
    
    # Decodificación completa
    print("=" * 80)
    print("DECODIFICACIÓN COMPLETA")
    print("=" * 80)
    full_decode = decode_substitution(cipher_text, extended_mapping)
    
    # Mostrar en párrafos
    words = full_decode.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= 75:
            line += word + " "
        else:
            print(line)
            line = word + " "
    print(line)
    print()
    
    # Mostrar el flag
    print("=" * 80)
    print("FLAG DECODIFICADO")
    print("=" * 80)
    flag_decoded_full = decode_substitution(flag_cipher, extended_mapping)
    print(flag_decoded_full)
    print("=" * 80)


if __name__ == "__main__":
    main()

import hashlib
from pathlib import Path

# Pon aquí el hash que te suelta el server, el “secret cheese”
HASH_OBJETIVO = "8f2a5f1795cd31f39aff1f16d09bcf21ed49d541fa2f2947e32a3aa964459579"

# Asegúrate de que "cheese_list.txt" esté en la misma carpeta que este script
CARPETA_DEL_SCRIPT = Path(__file__).resolve().parent
ARCHIVO_QUESOS = CARPETA_DEL_SCRIPT / "cheese_list.txt"


def sha256_hex(data: bytes) -> str:
    # Saca el SHA-256 en hex de un bloque de bytes.
    return hashlib.sha256(data).hexdigest()


def generar_sales():
    """
    Genera sales de 00..ff:
    - salt_hex: '00'..'ff' (para imprimir)
    - salt_byte: byte real b'\\x00'..b'\\xff' (para la opción “2 nibbles” literal)
    """
    for i in range(256):
        yield f"{i:02x}", bytes([i])


def variantes_de_queso(linea: str):
    """
    Por si el server normaliza el texto (a veces sí, a veces no).
    Si quieren hacerlo más estricto, dejen SOLO [base] y ya.
    """
    base = linea.rstrip("\r\n")
    if not base:
        return []

    posibles = [base, base.strip(), base.lower(), base.upper()]

    # Quitamos duplicados sin romper el orden
    vistos = set()
    salida = []
    for p in posibles:
        if p and p not in vistos:
            vistos.add(p)
            salida.append(p)
    return salida


def approach1(lineas):
    """
    APPROACH 1 (fuerza bruta directa):
    - Probamos cada queso del archivo (y algunas variantes por si el server normaliza).
    - Probamos sales 00..ff como BYTE real y también como ASCII ("7f").
    - Probamos prefijo/sufijo y separadores comunes.

    Devuelve (queso_encontrado, salt_hex) o None si no encuentra.
    """
    separadores = ["", ":", "|", "-", "_", " "]

    for linea in lineas:
        for queso in variantes_de_queso(linea):
            queso_b = queso.encode("utf-8")

            for salt_hex, salt_byte in generar_sales():
                salt_ascii = salt_hex.encode("ascii")  # b"00" .. b"ff"

                # 1) Sal como BYTE real (0x00..0xff) + prefijo/sufijo
                if sha256_hex(queso_b + salt_byte) == HASH_OBJETIVO or sha256_hex(salt_byte + queso_b) == HASH_OBJETIVO:
                    return queso, salt_hex

                # Casos con separadores (BYTE)
                for sep in separadores:
                    sep_b = sep.encode("ascii")
                    if sha256_hex(queso_b + sep_b + salt_byte) == HASH_OBJETIVO or sha256_hex(salt_byte + sep_b + queso_b) == HASH_OBJETIVO:
                        return queso, salt_hex

                # 2) Sal como ASCII ('7f' como dos caracteres) + prefijo/sufijo
                for sep in separadores:
                    sep_b = sep.encode("ascii")
                    if sha256_hex(queso_b + sep_b + salt_ascii) == HASH_OBJETIVO or sha256_hex(salt_ascii + sep_b + queso_b) == HASH_OBJETIVO:
                        return queso, salt_hex

    return None


def approach2(lineas):
    """
    APPROACH 2 (pre-cálculo estilo “tabla arcoíris”):
    En vez de hashear y comparar en el momento, armamos una “tabla” (dict)
    con TODOS los hashes posibles -> (queso, sal). Luego hacemos lookup directo.

    Esto hace más trabajo al inicio y usa más memoria, pero es un enfoque
    conceptualmente distinto: precomputación + búsqueda.

    Devuelve (queso_encontrado, salt_hex) o None si no encuentra.
    """
    separadores = ["", ":", "|", "-", "_", " "]
    tabla = {}  # hash_hex -> (queso, salt_hex)

    for linea in lineas:
        for queso in variantes_de_queso(linea):
            queso_b = queso.encode("utf-8")

            for salt_hex, salt_byte in generar_sales():
                salt_ascii = salt_hex.encode("ascii")

                # 1) BYTE real: prefijo/sufijo sin separador
                h1 = sha256_hex(queso_b + salt_byte)
                tabla.setdefault(h1, (queso, salt_hex))

                h2 = sha256_hex(salt_byte + queso_b)
                tabla.setdefault(h2, (queso, salt_hex))

                # BYTE con separadores
                for sep in separadores:
                    sep_b = sep.encode("ascii")
                    h3 = sha256_hex(queso_b + sep_b + salt_byte)
                    tabla.setdefault(h3, (queso, salt_hex))

                    h4 = sha256_hex(salt_byte + sep_b + queso_b)
                    tabla.setdefault(h4, (queso, salt_hex))

                # 2) ASCII hex con separadores
                for sep in separadores:
                    sep_b = sep.encode("ascii")
                    h5 = sha256_hex(queso_b + sep_b + salt_ascii)
                    tabla.setdefault(h5, (queso, salt_hex))

                    h6 = sha256_hex(salt_ascii + sep_b + queso_b)
                    tabla.setdefault(h6, (queso, salt_hex))

    return tabla.get(HASH_OBJETIVO)


def main():
    if not ARCHIVO_QUESOS.exists():
        print("No encuentro cheese_list.txt en la misma carpeta del script. Revisen la ruta y vuelvan a correr.")
        return

    # Leer la lista de quesos (una línea = un queso)
    lineas = ARCHIVO_QUESOS.read_text(encoding="utf-8", errors="replace").splitlines()

    resultado1 = approach1(lineas)
    if resultado1 is None:
        print("No se encontró coincidencia con approach1.")
        return

    resultado2 = approach2(lineas)
    if resultado2 is None:
        print("No se encontró coincidencia con approach2.")
        return

    queso1, sal1 = resultado1
    print(f"Cheese Name: {queso1}")
    print(f"salt: {sal1}")

    queso2, sal2 = resultado2
    print(f"Cheese Name: {queso2}")
    print(f"salt: {sal2}")


if __name__ == "__main__":
    main()
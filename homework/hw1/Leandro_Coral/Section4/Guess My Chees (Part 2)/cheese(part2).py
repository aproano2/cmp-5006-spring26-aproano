"""
Varios metodos fueron usandos para crear rainbow tables que sirvan para decodificar el mensaje oculto, esta rainbow toble que genero el codigo fue
lo suficientemente grando para cubrir la mayor parte de posibilidades. Aunque aun falla. Archivos fueron dejados como muestra de las tablas generadas
anteriormente sin exito
"""


import hashlib

with open("cheese_list.txt", "r", encoding="utf-8") as f:
    file = f.readlines()

with open("resultados_hash.txt", "w", encoding="utf-8") as out:
    for j in file:
        for k in "0123456789abcdef":
            for l in "0123456789abcdef":
                out.write(
                    f"{j[:-1]}{k}{l} {hashlib.sha256((j[:-1] + k + l).encode('utf-8')).hexdigest()}\n"
                )
                out.write(
                    f"{k}{l}{j[:-1]} {hashlib.sha256((k + l + j[:-1]).encode('utf-8')).hexdigest()}\n"
                )
    for j in file:
        for k in range(256):
            out.write(
                f"{j[:-1]}{hex(k)} {hashlib.sha256((j[:-1] + chr(k)).encode('utf-8')).hexdigest()}\n"
            )
            out.write(
                f"{hex(k)}{j[:-1]} {hashlib.sha256((chr(k) + j[:-1]).encode('utf-8')).hexdigest()}\n"
            )
            out.write(
                f"{j[:-1]}{hex(k)} {hashlib.sha256((j[:-1] + chr(k)).lower().encode('utf-8')).hexdigest()}\n"
            )
            out.write(
                f"{hex(k)}{j[:-1]} {hashlib.sha256((chr(k) + j[:-1]).lower().encode('utf-8')).hexdigest()}\n"
            )




# picoCTF - substitution2 (Classic Crypto)

## Objetivo
Descifrar un mensaje cifrado con un cifrado de sustitución monoalfabética, sin espacios ni puntuación, de forma completamente local y reproducible.

## Observaciones iniciales
- El ciphertext está compuesto casi totalmente por letras, con algunos caracteres no alfabéticos (`{}`, `_`, dígitos).
- La ausencia de espacios/puntuación impide usar heurísticas simples basadas en separación de palabras.
- El hint sugiere mejorar el ataque de frecuencia usando grupos de letras, lo cual apunta a análisis con n-gramas (bigrams/trigrams/quadgrams).

## Hipótesis
1. El cifrado es una sustitución monoalfabética: cada letra del alfabeto se mapea de forma consistente a otra letra.
2. Los caracteres no alfabéticos (dígitos, `_`, `{`, `}`) permanecen sin cambios.

Estas hipótesis se validan si al aplicar una única tabla de sustitución el texto descifrado comienza a exhibir estructura del inglés y/o aparece el patrón de bandera.

## Metodología
### Por qué la frecuencia simple no es suficiente
El conteo de letras (unigramas) puede aproximar algunas correspondencias (por ejemplo, la letra más frecuente suele corresponder a 'e'), pero:
- muchas letras tienen frecuencias similares,
- sin espacios la evaluación visual es difícil,
- el descifrado puede quedar “casi correcto” con varios intercambios (swaps) entre letras.

### Refinamiento con n-gramas
Para evaluar automáticamente qué tan “inglés” suena un texto descifrado se usa un modelo estadístico de n-gramas:
- bigramas (2 letras),
- trigramas (3 letras),
- cuatrigramas (4 letras).

Las secuencias comunes del inglés reciben mayor probabilidad; las raras o inexistentes reciben penalización. Esto permite comparar claves candidatas de manera objetiva.

### Búsqueda heurística (simulated annealing)
No es viable probar las 26! permutaciones posibles. En su lugar se utiliza una búsqueda heurística:
- Se genera una clave aleatoria (permutación del alfabeto).
- Se aplica al ciphertext para obtener un plaintext candidato.
- Se define una función de puntuación basada en n-gramas (score).
- Se muta la clave mediante swaps (intercambio de dos asignaciones) y se decide si aceptar el cambio:
  - siempre si mejora el score,
  - a veces si empeora ligeramente (controlado por una “temperatura” que disminuye), para escapar de óptimos locales.
- Se repite con múltiples reinicios aleatorios para aumentar probabilidad de converger a la solución correcta.

### Entrenamiento local del modelo de idioma
El modelo de n-gramas se entrena localmente usando un corpus en texto plano (`en-the-little-prince.txt`).
Esto evita depender de servicios en línea y mejora significativamente la calidad del score frente a entrenar con un texto corto.

## Implementación
Archivos:
- `pablo_message.txt`: ciphertext provisto por el reto.
- `en-the-little-prince.txt`: corpus local para entrenar n-gramas.
- `substitution2_solve_improved.py`: solver local con n-gramas + simulated annealing.
- `decrypted.txt`: salida con el mejor plaintext y la tabla cipher->plain.
- `extract_flag.py`: extractor local para obtener `picoCTF{...}` desde `decrypted.txt`.

Ejecutar el solver:
```bash
python substitution2_solve_improved.py -i pablo_message.txt -c en-the-little-prince.txt -o decrypted.txt --restarts 120 --steps 30000

```


Extraer la flag:

```bash
python extract_flag.py -i decrypted.txt
```

## Verificación de la solución (flujo normal vs. verificación con clave)

En el flujo normal de resolución, el script `substitution2_solve_improved.py` es el componente principal: entrena un modelo estadístico de idioma a partir del corpus local (`en-the-little-prince.txt`), genera claves de sustitución aleatorias y utiliza simulated annealing con reinicios para optimizar una función de puntuación basada en n-gramas. La convergencia se considera exitosa cuando el plaintext descifrado presenta estructura coherente del inglés y aparece una cadena con el patrón `picoCTF{...}`.

En otras palabras, si el proceso de optimización converge completamente, la propia ejecución del solver debería revelar directamente la bandera dentro del texto descifrado y/o imprimirla mediante la búsqueda por expresión regular.

Sin embargo, debido a la naturaleza estocástica del método (dependencia de reinicios aleatorios y escapes de óptimos locales), es posible obtener descifrados “casi correctos” donde la bandera aparece con pocas letras intercambiadas. Para separar claramente el proceso de descifrado del proceso de validación, se utilizó un verificador determinista adicional.

### Verificador determinista con clave (solo validación)

El script `decrypt_with_key.py` se utiliza únicamente para verificación: toma una clave de sustitución ya obtenida (tabla A..Z) y la aplica al ciphertext para producir el plaintext final de forma determinista. Luego extrae e imprime la bandera si existe.

Esto permite:

* Confirmar la solución final sin depender del azar del optimizador.
* Reproducir exactamente el mismo resultado en cualquier máquina.
* Registrar evidencia (comando + output) para el reporte.

Ejecución del verificador:

```bash
python decrypt_with_key.py -i pablo_message.txt -o decrypted_verified.txt
```

## Validación de resultados

La validación se realizó verificando que el plaintext contiene el patrón exacto de bandera y que su contenido coincide con el formato esperado de picoCTF.

Bandera obtenida:
`picoCTF{N6R4M_4N41Y515_15_73D10U5_42EA1770}`

## Diferencias respecto a soluciones tipo web

* La solución principal se basa en un modelo estadístico local (n-gramas) y un algoritmo de optimización reproducible mediante parámetros.
* No se utilizó prueba y error manual en herramientas web.
* La verificación final se realizó con un script local determinista aplicando la clave, para garantizar reproducibilidad y evidencia clara del resultado.

## Flag

picoCTF{N6R4M_4N41Y515_15_73D10U5_42EA1770}


